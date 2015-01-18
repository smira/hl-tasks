FROM smira/hl-tasks:base
MAINTAINER Andrey Smirnov <smirnov.andrey@gmail.com>

RUN useradd -ms /bin/bash hl-tasks

RUN echo "hl-tasks ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

COPY schema.sql .

RUN sed -i s#peer#trust# /etc/postgresql/9.4/main/pg_hba.conf && \
      /etc/init.d/postgresql start && \
      createuser -U postgres -s student && \
      createdb -U student student && \
      psql -U student < schema.sql && \
      /etc/init.d/postgresql stop

USER hl-tasks

COPY main.go start.sh /home/hl-tasks/

WORKDIR /home/hl-tasks

ENV GOPATH /home/hl-tasks/

RUN go get -v -d ./... && go build main.go

ENTRYPOINT /home/hl-tasks/start.sh