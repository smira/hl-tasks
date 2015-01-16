FROM smira/hl-tasks:base
MAINTAINER Andrey Smirnov <smirnov.andrey@gmail.com>

RUN useradd -ms /bin/bash hl-tasks

USER hl-tasks

COPY memc.py /home/hl-tasks/

WORKDIR /home/hl-tasks

ENTRYPOINT /bin/bash