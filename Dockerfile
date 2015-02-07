FROM smira/hl-tasks:base
MAINTAINER Andrey Smirnov <smirnov.andrey@gmail.com>

COPY client.go server.go /home/hl-tasks/

WORKDIR /home/hl-tasks

ENV GOPATH /home/hl-tasks/

RUN go get -v -d ./... && go build -o client client.go && go build -o server server.go

ENTRYPOINT /usr/bin/screen -s /bin/bash
