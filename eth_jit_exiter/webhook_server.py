import os
import logging
import asyncio

from aiohttp import ClientSession
from flask import Flask, request
from waitress import serve

logging.basicConfig()

LOGGER = logging.getLogger()

app = Flask(__name__)
CONFIG = {}

async def make_request(session, method, url, payload):
    try:
        response = await session.request(method=method, url=url, json=payload)
        body = await response.json()

        return {
            "status": response.status,
            "url": url,
            "body": body
        }
    except Exception as error:
        LOGGER.error(f"Error when sending request to {url}: {error}")

    # There was no response, so we generate a fail response.
    LOGGER.error(f"There was no response from the endpoint {url}")

    return {
        "status": 500,
        "body": {
            "message": f"There was no response from the host"
        },
        "url": url,
    }

async def async_requests(method, path, payload=None):
    async with ClientSession() as session:
        return await asyncio.gather(*[make_request(session, method, f"{endpoint}/{path}", payload) for endpoint in CONFIG['signer_endpoints']])

# { "validatorIndex": "123", "validatorPubkey": "0x123" }
@app.route("/webhook", methods=["POST"])
def exit_webhook():
    data = request.json

    LOGGER.info("Request body: ")
    LOGGER.info(data)

    validator_index = data.get('validatorIndex', None)
    validator_pub_key = data.get('validatorPubkey', None)

    if validator_index and validator_pub_key:
        # Asynchronously request every client to sign and submit the exit message
        # if they find the public key on their dirk instances
        sign_requests = async_requests(
            method='POST',
            path="exit-validator",
            payload={
                'validator_index': validator_index,
                'validator_pub_key': validator_pub_key
            }
        )

        responses = asyncio.run(sign_requests)

        LOGGER.info(responses)

        for response in responses:
            reponse_body = response['body']

            if reponse_body.get('status', None) == 'SUCCEEDED':
                return {"status": "SUCCEEDED"}, 200

    return {"status": "FAILED"}, 418

def check_signer_endpoints():
    """Check that all SIGNER endpoints can be reached."""
    responses = asyncio.run(async_requests(
        method='GET',
        path='ping'
    ))

    LOGGER.info("Testing connection to all SIGNER endpoints:")

    for response in responses:
        LOGGER.info(f"{response['url']} response: {response['body']}")

        if response.get('status', None) != 200:
            LOGGER.error(f"Error response from {response['url']} when testing endpoints: {response['body']}")

def start_server(config):
    global CONFIG
    CONFIG = config
    check_signer_endpoints()
    if os.getenv('FLASK_DEBUG', None) == '1':
        app.run('0.0.0.0', config.get('port', 13131))
    else:
        serve(app, host="0.0.0.0", port=config.get('port', 13131))
