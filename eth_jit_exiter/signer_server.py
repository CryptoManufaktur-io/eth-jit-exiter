import os
import logging
import binascii
import math
import collections

import grpc
import requests

from flask import Flask, request
from waitress import serve
from eth2spec.phase0.mainnet import DOMAIN_VOLUNTARY_EXIT, compute_domain, Version, VoluntaryExit, compute_signing_root, Root, Epoch, ValidatorIndex, bls, BLSPubkey, BLSSignature

from eth_jit_exiter import signer_pb2
from eth_jit_exiter import lister_pb2
from eth_jit_exiter import signer_pb2_grpc
from eth_jit_exiter import lister_pb2_grpc

from py_ecc.bls.g2_primitives import G2_to_signature, signature_to_G2
from py_ecc.optimized_bls12_381.optimized_curve import add, multiply, Z2, curve_order

LOGGER = logging.getLogger()

SLOTS_PER_EPOCH = 32
app = Flask(__name__)
CONFIG = {}

def lagrange_coefficient(i, indices, field_modulus):
    lc = 1
    for j in indices:
        if i != j:
            lc *= (0 - j) * pow(j - i, field_modulus - 2, field_modulus)
            lc %= field_modulus
    return lc

def bls_signature_recover(_signatures):
    """Lagrange Interpolation"""
    _signatures = collections.OrderedDict(sorted(_signatures.items()))
    indices = [x[0] for x in _signatures.items()]
    signatures = [x[1] for x in _signatures.items()]

    field_modulus = curve_order
    aggregated_signature = Z2

    for i, (signature, index) in enumerate(zip(signatures, indices)):
        lc = lagrange_coefficient(index, indices, field_modulus)
        scaled_signature = multiply(signature_to_G2(signature), lc)
        aggregated_signature = add(aggregated_signature, scaled_signature)

    return G2_to_signature(aggregated_signature)

def get_beacon_data():
    # Get current slot.
    current_slot = requests.get(f"{CONFIG['beacon_node_url']}/eth/v1/node/syncing").json()['data']['head_slot']

    # Calculate current epoch
    current_epoch = math.floor(int(current_slot) / SLOTS_PER_EPOCH)

    # Get current fork from the fork schedule
    fork_schedule = requests.get(f"{CONFIG['beacon_node_url']}/eth/v1/config/fork_schedule").json()['data']

    for schedule in fork_schedule:
        if schedule['current_version'].startswith("0x03"):
            current_fork_version = schedule['current_version']
            break

    # Get the Genesis validators root
    genesis_validators_root = requests.get(f"{CONFIG['beacon_node_url']}/eth/v1/beacon/genesis").json()['data']['genesis_validators_root']

    return {
        'current_fork_version': Version(current_fork_version),
        'current_epoch': Epoch(current_epoch),
        'genesis_validators_root': Root(genesis_validators_root),
    }

def submit_voluntary_exit(exit_message, signature):
    payload = {
        'message': {
            'epoch': str(exit_message.epoch),
            'validator_index': str(exit_message.validator_index)
        },
        'signature': f"{signature}"
    }

    response = requests.post(f"{CONFIG['beacon_node_url']}/eth/v1/beacon/pool/voluntary_exits", json=payload)

    return response

def get_composite_signature(credentials, account, data, domain):
    LOGGER.info("Getting threshold signatures...")

    endpoints = {x.id: f"{x.name}:{x.port}" for x in account.participants}
    signatures = {}

    # Get the threshold signatures.
    for id, endpoint in endpoints.items():
        channel = grpc.secure_channel(endpoint, credentials)

        LOGGER.info(f"Waiting for Sign channel on endpoint {endpoint}...")
        grpc.channel_ready_future(channel).result()
        LOGGER.info("Channel connected!")

        signer_stub = signer_pb2_grpc.SignerStub(channel)

        sign_response = signer_stub.Sign(signer_pb2.SignRequest(
            account=account.name,
            data=data,
            domain=domain
        ))

        channel.close()
        LOGGER.info("Sign Channel closed.")

        if sign_response.state == 1:
            LOGGER.info(f"Received signature from {endpoint}")
            signature = BLSSignature.from_obj(sign_response.signature)

            signatures[id] = signature

    if len(signatures.items()) < account.signing_threshold:
        raise Exception(f"Not enough signatures obtained to reach threshold.")

    # Recover composite signature.
    recovered_signature = bls_signature_recover(signatures)

    return BLSSignature.from_obj(recovered_signature)

def get_grpc_credentials():
    """Generate the gRPC SSL channel credentials"""
    root_certs = open(CONFIG['dirk']['ca_cert'], 'rb').read()
    client_key = open(CONFIG['dirk']['client_key'], 'rb').read()
    client_cert = open(CONFIG['dirk']['client_cert'], 'rb').read()

    credentials = grpc.ssl_channel_credentials(
        private_key=client_key,
        root_certificates=root_certs,
        certificate_chain=client_cert,
    )

    return credentials

def get_wallet_accounts():
    """Return a list of all the accounts in the wallet."""
    endpoint = CONFIG['dirk']['endpoint']

    LOGGER.info(f"Getting accounts list from endpoint {endpoint}")

    credentials = get_grpc_credentials()

    channel = grpc.secure_channel(endpoint, credentials)
    LOGGER.info("Waiting for List Accounts channel...")

    grpc.channel_ready_future(channel).result()
    LOGGER.info("Channel connected!")

    account_stub = lister_pb2_grpc.ListerStub(channel)
    accounts = account_stub.ListAccounts(lister_pb2.ListAccountsRequest(paths=[CONFIG['dirk']['wallet']]))

    channel.close()
    LOGGER.info("Channel closed.")

    accounts_by_pub = {binascii.b2a_hex(account.composite_public_key).decode():account for account in accounts.DistributedAccounts}

    return accounts_by_pub

def generate_voluntary_exit(account, validator_index):
    LOGGER.info(f"Generating voluntary exit for {account.name}")
    beacon_data = get_beacon_data()

    LOGGER.info(beacon_data)

    voluntary_exit = VoluntaryExit(
        epoch=beacon_data['current_epoch'],
        validator_index=ValidatorIndex(validator_index),
    )

    domain = compute_domain(DOMAIN_VOLUNTARY_EXIT, beacon_data['current_fork_version'], beacon_data['genesis_validators_root'])

    LOGGER.info(f"Domain: {domain}")

    credentials = get_grpc_credentials()

    signature = get_composite_signature(
        credentials=credentials,
        account=account,
        data=voluntary_exit.hash_tree_root(),
        domain=domain
    )

    return voluntary_exit, signature, domain

@app.route('/ping', methods=["GET"])
def ping():
    """Send a 200 response so the webhook knows the connection is fine."""
    return {"message": "Pong!"}

@app.route('/exit-validator', methods=["POST"])
def exit_validator():
    request_data = request.json

    LOGGER.info(request_data)

    public_key = request_data.get('validator_pub_key')
    validator_index = int(request_data.get('validator_index'))

    if public_key.startswith('0x'):
        public_key = public_key[2:]

    accounts = get_wallet_accounts()

    if public_key in accounts:
        account = accounts[public_key]

        LOGGER.info(f"Using public key {public_key}")
        LOGGER.info(f"Account name: {account.name}")

        try:
            voluntary_exit, signature, domain = generate_voluntary_exit(account, validator_index)
            signing_root = compute_signing_root(voluntary_exit, domain)
            valid = bls.Verify(BLSPubkey.fromhex(public_key), signing_root, signature)
            LOGGER.info(f"Is signature valid? {valid}")

            if valid:
                # Submit Voluntary Exit message to CL node.
                response = submit_voluntary_exit(voluntary_exit, signature)

                LOGGER.info(response.status_code)
                data = response.json()

                if response.status_code == 200:
                    return {'status': 'SUCCEEDED'}

                return {'status':'VOLUNTARY EXIT REJECTED BY CONSENSUS CLIENT', 'message': data['message']}, 400

            return {'status': 'GENERATED SIGNATURE WAS INVALID'}, 400
        except Exception as err:
            LOGGER.error(err)
            return {'status': 'ERROR WHEN GENERATING SIGNATURE'}, 400
    else:
        return {'status': 'NOT FOUND'}, 404

def check_signing():
    """Check that we're able to get signatures from Dirk using Validator Index `0` so it's never submittable."""
    LOGGER.info("Checking that we can get signatures from Dirk.")
    accounts = get_wallet_accounts()
    account = accounts[list(accounts.keys())[0]]

    voluntary_exit, signature, domain = generate_voluntary_exit(account, 1)

    signing_root = compute_signing_root(voluntary_exit, domain)

    valid = bls.Verify(BLSPubkey.from_obj(account.composite_public_key), signing_root, signature)

    if valid:
        LOGGER.info("Test signature is valid!")
    else:
        LOGGER.error("Generated signature is not valid!")

def start_server(config):
    global CONFIG
    CONFIG = config
    check_signing()

    if os.getenv('FLASK_DEBUG', None) == '1':
        app.run('0.0.0.0', config.get('port', 13131))
    else:
        serve(app, host="0.0.0.0", port=config.get('port', 13131))
