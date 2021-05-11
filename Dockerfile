FROM ubuntu:18.04

RUN apt-get update

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get install -y vim\
    python3-pip \
    nano

RUN apt-get install software-properties-common -y
RUN add-apt-repository -y ppa:ethereum/ethereum
RUN apt-get update
RUN apt-get install solc -y

RUN pip3 install pysha3 attrdict eth-abi toml docopt websockets requests aiohttp web3 py-solc

COPY contracts contracts

COPY testing testing

WORKDIR /testing

ENTRYPOINT ["python3", "./test.py"]
