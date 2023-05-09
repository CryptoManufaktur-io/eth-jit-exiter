import os
import logging
import asyncio

from datetime import datetime

from aiohttp import ClientSession
from flask import Flask, request
from waitress import serve
from pyrate_limiter import Limiter, RequestRate, BucketFullException, SQLiteBucket
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Counter

logging.basicConfig()

LOGGER = logging.getLogger()

app = Flask(__name__)
CONFIG = {}
LIMITER = None

# Define all metrics
EXIT_REQUESTS_COUNTER = Counter('exit_requests', 'Number of times an exit has been requested')
EXIT_REQUESTS_LIMITED = Counter('exit_requests_rate_limited', 'Number of times an exit request has been rate limited')
EXIT_REQUESTS_SUCCESSFUL = Counter('exit_requests_successful', 'Number of times an exit request has been submitted successfully')
EXIT_REQUESTS_FAILED = Counter('exit_requests_failed', 'Number of times an exit request failed')

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
    EXIT_REQUESTS_COUNTER.inc()

    try:
        LIMITER.try_acquire('webhook')
    except BucketFullException as err:
        volume = LIMITER.get_current_volume('webhook')
        LOGGER.error(err.meta_info)
        LOGGER.error(f"Current rate volume: {volume}")
        EXIT_REQUESTS_LIMITED.inc()
        return {"status": "RATE_LIMIT_EXCEEDED"}, 429

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
                EXIT_REQUESTS_SUCCESSFUL.inc()
                return {"status": "SUCCEEDED"}, 200

    EXIT_REQUESTS_FAILED.inc()
    return {"status": "FAILED"}, 418

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

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
    global LIMITER

    CONFIG = config

    request_rate = CONFIG.get('rate_limit', {}).get('request_rate', 500)
    interval = CONFIG.get('rate_limit', {}).get('interval', 604800)

    rate = RequestRate(
        limit=request_rate,
        interval=interval
    )

    LIMITER = Limiter(
        rate,
        bucket_class=SQLiteBucket,
        bucket_kwargs={'path': '/var/lib/eth-jit-exiter/limiter.sqlite'},
        time_function=lambda: datetime.utcnow().timestamp()
    )

    LOGGER.info(f"Rate limit set at {request_rate} requests per {interval} seconds")

    check_signer_endpoints()
    if os.getenv('FLASK_DEBUG', None) == '1':
        app.run('0.0.0.0', config.get('port', 13131))
    else:
        serve(app, host="0.0.0.0", port=config.get('port', 13131))
