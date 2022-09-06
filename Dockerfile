FROM tensorflow/tensorflow:latest-gpu

RUN pip install diffusers pillow torch transformers \
  --extra-index-url https://download.pytorch.org/whl/cu116

RUN useradd -m huggingface

USER huggingface

WORKDIR /home/huggingface

RUN mkdir -p /home/huggingface/.cache/huggingface \
  && mkdir -p /home/huggingface/output

COPY server.py /usr/local/bin
COPY docker-entrypoint.py /usr/local/bin
COPY token.txt /home/huggingface
COPY server.py /home/huggingface

RUN pip install fastapi
RUN pip install uvicorn

CMD uvicorn server:app --reload

# ENTRYPOINT [ "docker-entrypoint.py" ]
