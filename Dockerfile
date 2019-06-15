FROM python:3
MAINTAINER rmelo <rdg.melo@gmail.com>

RUN 	apt-get -y update &&\
	apt-get -y upgrade &&\ 
	apt-get install -y build-essential cmake &&\
	apt-get install -y libopencv-dev &&\
	apt-get install -y vim

ADD . /opt/receipts-stitcher

WORKDIR /opt/receipts-stitcher/Stitcher

RUN	mkdir build &&\
	cd ./build &&\
	cmake .. &&\
	make

ENV	PATH "$PATH:/opt/receipts-stitcher/Stitcher/build"

WORKDIR /opt/receipts-stitcher

CMD python main.py

