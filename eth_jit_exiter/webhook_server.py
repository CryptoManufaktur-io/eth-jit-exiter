import logging
import asyncio

from aiohttp import ClientSession
from flask import Flask, request

logging.basicConfig()

LOGGER = logging.getLogger()

app = Flask(__name__)
CONFIG = {}

async def request_exit(session, url, payload):
    try:
        response = await session.request(method='POST', url=url, json=payload)
        return await response.json()
    except Exception as error:
        LOGGER.error(error)

    # There was no response, so we generate a fail response.
    LOGGER.error(f"There was no response from the endpoint {url}")

    return {
        "status": "FAILED",
        "description": f"There was no response from the endpoint {url}"
    }


async def async_requests(payload):
    async with ClientSession() as session:
        return await asyncio.gather(*[request_exit(session, f"{endpoint}/exit-validator", payload) for endpoint in CONFIG['signer_endpoints']])

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
        sign_requests = async_requests({
            'validator_index': validator_index,
            'validator_pub_key': validator_pub_key
        })

        responses = asyncio.run(sign_requests)

        LOGGER.info(responses)

        for response in responses:
            if response.get('status', None) == 'SUCCEEDED':
                return {"status": "SUCCEEDED"}, 200

    return {"status": "FAILED"}, 418


def start_server(config):
    global CONFIG
    CONFIG = config
    app.run('0.0.0.0', CONFIG.get('port', 13131))
