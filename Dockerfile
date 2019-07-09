FROM python:3

LABEL maintainer="rmelo <rdg.melo@gmail.com>"

RUN groupadd -r appuser && useradd -r -g appuser appuser

# hadolint ignore=DL3008
RUN apt-get -y update &&\
	apt-get install -y --no-install-recommends build-essential cmake &&\
	apt-get install -y --no-install-recommends libopencv-dev &&\
	apt-get clean &&\ 
	rm -rf /var/lib/apt/lists/*

COPY . /opt/app

RUN chown -R appuser:appuser /opt/app

WORKDIR /opt/app/Stitcher

RUN	mkdir build

WORKDIR /opt/app/Stitcher/build

RUN cmake .. &&\
	make

ENV	PATH "$PATH:/opt/app/Stitcher/build"

WORKDIR /opt/app

RUN pip install -r requirements.txt

USER appuser

ENTRYPOINT ["uwsgi"] 

CMD ["--ini", "app.ini"]
