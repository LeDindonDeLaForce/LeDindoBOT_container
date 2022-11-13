# Base
FROM alpine:3.16.2

## Install packages
RUN apk add --no-cache python3 py3-pip





## Startup
COPY files/run.sh /run.sh
COPY files/requirements.txt /requirements.txt

RUN addgroup -g 3615 ledindobot \
    && adduser -u 3615 -G "ledindobot" -D ledindobot \
    && chmod 750 /run.sh /requirements.txt && chown ledindobot:ledindobot /run.sh /requirements.txt

### Set user
USER ledindobot
RUN cd /home/ledindobot && python3.10 -m pip install pipenv && python3.10 -m pipenv --python 3.10 && python3.10 -m pipenv install -r /requirements.txt

# Entrypoint
ENTRYPOINT [ "/run.sh" ]

