FROM smira/hl-tasks:base
MAINTAINER Andrey Smirnov <smirnov.andrey@gmail.com>

RUN curl -sSL https://twemproxy.googlecode.com/files/nutcracker-0.3.0.tar.gz \
        | tar -v -C /usr/src -xz

RUN cd /usr/src/nutcracker-0.3.0 && ./configure && make all install

ENV PATH /usr/local/bin:$PATH

RUN useradd -ms /bin/bash hl-tasks

USER hl-tasks

COPY crack.py /home/hl-tasks/

WORKDIR /home/hl-tasks

ENTRYPOINT /bin/bash