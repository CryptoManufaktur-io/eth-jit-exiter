FROM python:3.9-bullseye as builder

RUN python --version

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY . .

RUN poetry install

RUN ./build.sh

FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y ca-certificates bash tzdata hwloc libhwloc-dev wget

COPY --from=builder /app/build/eth-jit-exiter/eth-jit-exiter /usr/local/bin/

RUN mkdir /var/lib/eth-jit-exiter && chmod 0777 /var/lib/eth-jit-exiter

ENTRYPOINT [ "/usr/local/bin/eth-jit-exiter" ]
