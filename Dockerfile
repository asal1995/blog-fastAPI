FROM reg.maxpool.ir/applications/maxfastapi
WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN /app/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

RUN /app/venv/bin/pip install  -e .
WORKDIR /app/

ENV MODULE_NAME=fast_bloge.main
ENV REDIS_URL=redis://172.17.0.1
ENV SQLALCHEMY_DATABASE_URL=postgresql://postgres:0000@db/test
ENV JWT_PUBKEY="-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEJ6OY97LuO1NgEEtd9u85mYUNo3SA\nDvU6zL/MpAOKVZwPa4a3po3B7f5k0zWliZC4TWHqMOY2W3tnPtyKXYbI7Q==\n-----END PUBLIC KEY-----"
ENV PORT=8023
ENV ORIGIN="https://www.bitmax.ir/"
ENV SERVICE_NAME=fast_bloge
ENV OTEL_SERVER="otel-collector:4317"
ENV PORT=8000
ENV HOST=0.0.0.0
ENV API_KEY="08f2e9e806108661309942e06dfc825ebd02af5cdb425a8236db68ce90df0f2e"
ENV DEBUG=True
ENV DATABASE_URL=postgresql://postgres:0000@db/fastapi-admin


ENV PYTHONPATH=/app
CMD ["./start.sh"]


