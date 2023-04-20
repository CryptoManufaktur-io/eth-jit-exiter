FROM python:3.9-bullseye as builder

RUN python --version

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY . .

# RUN rm /app/poetry.lock

RUN poetry install

RUN ./build.sh

RUN mv build/eth-jit-exitter/eth-jit-exitter /bin/eth-jit-exitter

ENTRYPOINT [ "/bin/eth-jit-exitter" ]
