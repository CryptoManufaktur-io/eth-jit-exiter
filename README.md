# eth-jit-exiter

eth-jit-exiter provides a webhook for other tooling (e.g: [validator-ejector](https://github.com/lidofinance/validator-ejector)) to request the signing and submitting Voluntary Exit messages for Ethereum Validators.

It is designed to request the signatures from [Dirk](https://github.com/attestantio/dirk/) or any other gRPC that follows the [eth2-signer-api](https://github.com/wealdtech/eth2-signer-api) definition.

It can run in `WEBHOOK` or `SIGNER` mode. The WEBHOOK mode gets the external request and then asynchronously contacts all SIGNER servers. If any of the SIGNER servers is sucessful in submitting the Voluntary Exit message, the WEBHOOK server will respond with a `200` status code.

## Development

### Requirements

- python ^3.9.10 built with a shared Python Library

Linux:
```shell
sudo apt-get install python3-dev
```

MacOS with pyenv:
```shell
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.9.10
```

- [Poetry](https://python-poetry.org/)

```shell
curl -sSL https://install.python-poetry.org | python -
```

### Install Dependencies

```shell
poetry install
```

### Running locally

```shell
poetry run python eth_jit_exiter/main.py --config /path/to/config.yml
```

### Building Executable

```shell
./build.sh
```

## Configuration

`WEBHOOK` mode example:

```yaml
# The desired running mode
running_mode: SERVER

# The port to listen for requests from the external tools
# Can also be set by the environment variable EXITER_PORT
# If both are present, the environment variable has precedence.
port: 13131

# Rate limit on the webhook endpoint.
# Default is 500 requests per 7 days.
rate_limit:
  request_rate: 500
  interval: 604800

# List of SIGNER endpoints
signer_endpoints:
  - http://signer-a.example.com:13131
  - http://signer-b.example.com:13131
```

`SIGNER` mode example:

```yaml
# The desired running mode
running_mode: SIGNER

# The port to listen for requests
# Can also be set by the environment variable EXITER_PORT
# If both are present, the environment variable has precedence.
port: 13131

# URL of the Beacon Node to get Chain data and submit the Voluntary Exit message.
beacon_node_url: https://cl.example.com

dirk:
  # Hostname and port of the Dirk instance.
  endpoint: dirk.example.com:13141

  # Path to the client certificate to authenticate with Dirk.
  client_cert: /path/to/certs/client.crt

  # Path to the key to authenticate with Dirk.
  client_key: /path/to/certs/client.key

  # Path to the Certificate Authority certificate.
  ca_cert: /path/to/certs/dirk_authority.crt

  # Name of the Wallet
  wallet: Wallet
```

## Rate Limit

By default, requests to the webhook are rate limited.

In order for the volume counter to be persisted, SQLite is used as a backend.

A persistent volume is necessary when running in Docker, mapped to `/var/lib/eth-jit-exiter/`.

## Metrics

Metrics from the webhook endpoint are published at `/metrics` on the same port.

## Security

`eth-jit-exiter` is expected to run behind a firewall and only accessible by trusted sources.

Make sure to secure the environment where you're running both the webhook and signers.

## License

[Apache License v2](LICENSE)
