FROM jupyterhub/jupyterhub

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-client \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install --no-cache -r /tmp/requirements.txt
RUN python3 -m pip install --no-cache iotlabcli==3.1.1

COPY iotlabauthenticator /src/iotlabauthenticator
RUN python3 -m pip install --no-cache /src/iotlabauthenticator

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY templates/login.html /srv/jupyterhub/login.html

RUN mkdir -p /srv/jupyterhub/users
