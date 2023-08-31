# https://github.com/ykursadkaya/pyspark-Docker
ARG IMAGE_VARIANT=slim-buster
ARG PYTHON_VERSION=3.9.8
FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT}

# no make in slim
RUN apt update -y && apt install make

# make sure these match tox.ini
RUN pip install tox==3.26.0 poetry==1.3.2 tox-poetry-installer==0.10.2

COPY . /work
WORKDIR /work
RUN make .venv-prod
ENTRYPOINT [ ".venv/bin/python", "app.py", "/config/config.yaml" ]
