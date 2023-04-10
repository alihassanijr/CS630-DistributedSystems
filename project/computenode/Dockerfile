FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ='America/Los_Angeles'
RUN apt-get -y update
RUN apt-get -y install build-essential libtool autoconf unzip wget
RUN apt-get -y install cmake
RUN apt-get -y install curl net-tools
RUN apt-get -y install git 
RUN apt-get -y install python3
#COPY . /cm
#WORKDIR /cm
#RUN make
#WORKDIR /
#RUN mkdir -p /root
#WORKDIR /root
RUN echo "export PATH=/cm/bin/:${PATH}" >> /root/.bashrc
RUN echo "export PATH=/cm/bin/:${PATH}" >> /etc/skel/.bashrc
