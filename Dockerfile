FROM reg.maxpool.ir/applications/maxfastapi
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
RUN /app/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /app
RUN /app/venv/bin/pip install  -e .
WORKDIR /app/
ENV MODULE_NAME=fast_bloge.main
CMD ["./start.sh"]
