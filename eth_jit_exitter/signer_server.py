import logging
import binascii
import math

import grpc
import requests

from flask import Flask, request
from eth2spec.phase0.mainnet import DOMAIN_VOLUNTARY_EXIT, compute_domain, Version, VoluntaryExit, compute_signing_root, Root, Epoch, ValidatorIndex

from eth_jit_exitter import signer_pb2
from eth_jit_exitter import lister_pb2
from eth_jit_exitter import signer_pb2_grpc
from eth_jit_exitter import lister_pb2_grpc

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

SLOTS_PER_EPOCH = 32
app = Flask(__name__)
CONFIG = {}

def get_beacon_data():
    # Get current slot.
    current_slot = requests.get(f"{CONFIG['beacon_node_url']}/eth/v1/node/syncing").json()['data']['head_slot']

    # Calculate current epoch
    current_epoch = math.floor(int(current_slot) / SLOTS_PER_EPOCH)

    # Get current fork from the fork schedule
    fork_schedule = requests.get(f"{CONFIG['beacon_node_url']}/eth/v1/config/fork_schedule").json()['data']

    for schedule in fork_schedule:
        if int(schedule['epoch']) <= current_epoch:
            current_fork_version = schedule['current_version']

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
            'epoch': exit_message.epoch,
            'validator_index': exit_message.validator_index
        },
        'signature': f"0x{signature}"
    }

    response = requests.post(f"{CONFIG['beacon_node_url']}/eth/v1/beacon/pool/voluntary_exits", json=payload)
    return response

@app.route('/exit-validator', methods=["POST"])
def exit_validator():
    print(CONFIG['dirk']['endpoint'])

    request_data = request.json

    public_key = request_data.get('validator_pub_key')

    if public_key.startswith('0x'):
        public_key = public_key[2:]

    root_certs = open(CONFIG['dirk']['ca_cert'], 'rb').read()
    client_key = open(CONFIG['dirk']['client_key'], 'rb').read()
    client_cert = open(CONFIG['dirk']['client_cert'], 'rb').read()

    credentials = grpc.ssl_channel_credentials(
        private_key=client_key,
        root_certificates=root_certs,
        certificate_chain=client_cert,
    )

    channel = grpc.secure_channel(CONFIG['dirk']['endpoint'], credentials)
    LOGGER.info("Waiting for channel...")
    grpc.channel_ready_future(channel).result()
    LOGGER.info("Channel connected!")

    account_stub = lister_pb2_grpc.ListerStub(channel)
    accounts = account_stub.ListAccounts(lister_pb2.ListAccountsRequest(paths=[CONFIG['dirk']['wallet']]))

    accounts_by_pub = {binascii.b2a_hex(account.composite_public_key).decode():account for account in accounts.DistributedAccounts}

    if public_key in accounts_by_pub:
        signer_stub = signer_pb2_grpc.SignerStub(channel)

        account = accounts_by_pub[public_key]

        public_key = binascii.b2a_hex(account.composite_public_key).decode()

        LOGGER.info(f"Using public key {public_key}")

        beacon_data = get_beacon_data()

        voluntary_exit = VoluntaryExit(
            epoch=beacon_data['current_epoch'],
            validator_index=ValidatorIndex(394049),
        )

        domain = compute_domain(DOMAIN_VOLUNTARY_EXIT, beacon_data['current_fork_version'], beacon_data['genesis_validators_root'])
        signing_root = compute_signing_root(voluntary_exit, domain)

        sign_response = signer_stub.Sign(signer_pb2.SignRequest(
            account=account.name,
            data=signing_root.encode_bytes(),
            domain=domain.encode_bytes()
        ))

        channel.close()
        LOGGER.info("Channel closed.")

        if sign_response.state == 1:
            decoded_signature = binascii.b2a_hex(sign_response.signature).decode()

            # Submit Voluntary Exit message to CL node.
            response = submit_voluntary_exit(voluntary_exit, decoded_signature)

            if response.status_code == 200:
                return {'status': 'SUCCEEDED'}

            return {'status':'VOLUNTARY EXIT REJECTED'}, 400
        else:
            LOGGER.error("Failed to sign exit!")
    else:
        channel.close()
        LOGGER.info("Channel closed.")
        return {'status': 'NOT FOUND'}, 404

def start_server(config):
    global CONFIG
    CONFIG = config
    app.run('0.0.0.0', config.get('port', 13131))
