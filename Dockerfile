FROM python:3.9-bullseye as builder

RUN python --version

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY . .

RUN poetry install

RUN ./build.sh

FROM debian:bullseye-slim

COPY --from=builder /app/build/eth-jit-exiter/eth-jit-exiter /bin/

ENTRYPOINT [ "/bin/eth-jit-exiter" ]
