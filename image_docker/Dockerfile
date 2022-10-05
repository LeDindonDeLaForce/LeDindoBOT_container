# Base
FROM debian:bullseye-slim

## Install packages
RUN apt-get update \
&& apt-get install -y python3-pip libmariadb3 libmariadb-dev \
&& rm -rf /var/lib/apt/lists/*




## Create user
RUN groupadd -r ledindobot -g 3615 \
  &&  useradd --create-home --no-log-init -r -g ledindobot -u 3615 ledindobot

## Startup
COPY files/run.sh /run.sh
COPY files/requirements.txt /requirements.txt

RUN chmod 750 /run.sh /requirements.txt && chown ledindobot:ledindobot /run.sh /requirements.txt

### Set user
USER ledindobot
RUN cd /home/ledindobot && python3.9 -m pip install pipenv && python3.9 -m pipenv install -r /requirements.txt

# Entrypoint
ENTRYPOINT [ "/run.sh" ]

