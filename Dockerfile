FROM smira/hl-tasks:base
MAINTAINER Andrey Smirnov <smirnov.andrey@gmail.com>

COPY src /home/hl-tasks/src

WORKDIR /home/hl-tasks

ENV GOPATH /home/hl-tasks/

RUN go build -o raftd src/github.com/smira/raftd/main.go

ENTRYPOINT /usr/bin/screen -s /bin/bash
