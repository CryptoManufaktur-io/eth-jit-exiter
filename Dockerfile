# Get ethdo
FROM wealdtech/ethdo as ethdo

FROM python:3.9-bullseye as builder

RUN python --version

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY . .

# RUN rm /app/poetry.lock

RUN poetry install

RUN ./build.sh

RUN mv build/eth-jit-exiter/eth-jit-exiter /bin/eth-jit-exiter

COPY --from=ethdo /app/ethdo /bin/ethdo

ENTRYPOINT [ "/bin/eth-jit-exiter" ]
