FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ='America/Los_Angeles'
RUN apt-get -y update
RUN apt-get -y install build-essential libtool autoconf unzip wget
RUN apt-get -y install cmake
RUN apt-get -y install curl net-tools
RUN apt-get -y install git 
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && apt-get -y install python3.10 python3.10-distutils
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && python3.10 -m pip install --upgrade pip
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 10
RUN mkdir -p /tmp/cm
COPY . /tmp/cm/
WORKDIR /tmp/cm/
RUN pip3 install -r requirements.txt
WORKDIR /
RUN rm -rf /tmp/cm/
RUN echo "export PATH=/cm/bin/:${PATH}" >> /root/.bashrc
RUN echo "export PATH=/cm/bin/:${PATH}" >> /etc/skel/.bashrc
