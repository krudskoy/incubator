FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools
RUN pip3 install boto3 flask flask-wtf pyopenssl

RUN git clone https://github.com/krudskoy/awstable /opt/awstable

ENTRYPOINT ["python3", "/opt/awstable/awstable.py"]

