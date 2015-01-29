FROM smira/hl-tasks:base
MAINTAINER Andrey Smirnov <smirnov.andrey@gmail.com>

COPY *.py  /home/hl-tasks/

WORKDIR /home/hl-tasks

ENTRYPOINT /usr/bin/screen -s /bin/bash