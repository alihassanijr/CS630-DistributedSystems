FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ='America/Los_Angeles'
RUN apt-get -y update
RUN apt-get -y install build-essential libtool autoconf unzip wget
RUN apt-get -y install cmake
RUN apt-get -y install curl net-tools
RUN apt-get -y install git 
RUN apt-get -y install python3 python3-pip
RUN mkdir -p /tmp/cm
COPY . /tmp/cm/
WORKDIR /tmp/cm/
RUN pip3 install -r requirements.txt
WORKDIR /
RUN rm -rf /tmp/cm/
RUN echo "export PATH=/cm/bin/:${PATH}" >> /root/.bashrc
RUN echo "export PATH=/cm/bin/:${PATH}" >> /etc/skel/.bashrc
