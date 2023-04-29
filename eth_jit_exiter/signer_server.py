import logging
import subprocess
import shlex
import re

from flask import Flask, request

LOGGER = logging.getLogger()

app = Flask(__name__)
CONFIG = {}

@app.route('/exit-validator', methods=["POST"])
def exit_validator():
    endpoint = CONFIG['dirk']['endpoint']

    LOGGER.info(f"Getting accounts list from endpoint {endpoint}")

    request_data = request.json

    LOGGER.info(request_data)

    public_key = request_data.get('validator_pub_key')

    if public_key.startswith('0x'):
        public_key = public_key[2:]

    # List Accounts
    # We have to parse the ethdo stdout and get the account names and public keys with regex.
    args = f"ethdo wallet accounts --verbose --client-cert={CONFIG['dirk']['client_cert']} --client-key={CONFIG['dirk']['client_key']} --server-ca-cert={CONFIG['dirk']['ca_cert']} --remote={CONFIG['dirk']['endpoint']} --wallet={CONFIG['dirk']['wallet']}"

    output = subprocess.run(shlex.split(args), capture_output=True)

    parsed_output = str(output.stdout).replace("\\nval", "\nval")

    parsed_output = re.findall( r'(val-.*Composite public key: .{98})', parsed_output)

    accounts = {}

    for r in parsed_output:
        account_name = re.findall(r'val-\d*', r)
        composite_public_key = re.findall(r'Composite public key: (.{98})', r)
        accounts[composite_public_key[0][2:]] = account_name[0]

    if public_key in accounts:
        # The public key is in the list of the accounts.
        # Ask ethdo to submit the validator voluntary exit.
        args = f"ethdo validator exit --quiet --validator={CONFIG['dirk']['wallet']}/{accounts[public_key]} --json --connection={CONFIG['beacon_node_url']} "
        args += f"--client-cert={CONFIG['dirk']['client_cert']} --client-key={CONFIG['dirk']['client_key']} --server-ca-cert={CONFIG['dirk']['ca_cert']} "
        args += f"--timeout 5m --remote={CONFIG['dirk']['endpoint']}"

        exit_output = subprocess.run(shlex.split(args), capture_output=True)

        if exit_output == 0:
            return {'status': 'SUCCEEDED'}

        return {'status': 'FAILED', 'message': exit_output.stderr.decode()}, 400

    return {'status': 'NOT FOUND'}, 404

def start_server(config):
    global CONFIG
    CONFIG = config
    app.run('0.0.0.0', config.get('port', 13131))
