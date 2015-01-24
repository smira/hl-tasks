FROM smira/hl-tasks:base
MAINTAINER Andrey Smirnov <smirnov.andrey@gmail.com>

RUN go get github.com/rakyll/boom

RUN useradd -ms /bin/bash hl-tasks

USER hl-tasks

COPY *.py start.sh /home/hl-tasks/

WORKDIR /home/hl-tasks

ENTRYPOINT /home/hl-tasks/start.sh