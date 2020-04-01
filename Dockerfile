FROM jupyterhub/jupyterhub:1.2

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    iproute2 \
    iputils-ping \
    openssh-client \
    wget \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install --no-cache -r /tmp/requirements.txt
RUN python3 -m pip install --no-cache iotlabcli==3.1.1

COPY iotlabauthenticator /src/iotlabauthenticator
RUN python3 -m pip install --no-cache /src/iotlabauthenticator

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
RUN mkdir -p /srv/jupyterhub/iotlab_template
COPY templates/login.html /srv/jupyterhub/iotlab_template/login.html

# Download script to automatically stop idle single-user servers
RUN wget https://raw.githubusercontent.com/jupyterhub/jupyterhub/1.1.0/examples/cull-idle/cull_idle_servers.py

RUN mkdir -p /srv/jupyterhub/users
