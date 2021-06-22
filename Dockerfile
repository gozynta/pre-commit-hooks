from python:3.9

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN adduser --disabled-password --gecos '' worker

RUN set -ex \
  && mkdir -p /srv \
#  && apt-get update \
#  && apt-get install --no-install-recommends -y <put apt packages here \
#  && apt-get clean \
#  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip \
  && pip install pipenv \
  && rm -rf ~/.cache

WORKDIR /srv

# Copy Pipfile first, and install dependencies
# This is a separate step so it doesn't re-run with every source change
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN set -ex \
  && pipenv install --deploy --system \
  && rm -rf ~/.cache

# Not a bad idea to keep the copyright with the code
COPY LICENSE LICENSE

# Upload source
COPY pysrc pysrc

# Run as non-root user
USER worker

ENTRYPOINT python pysrc/fizzbuzz.py
