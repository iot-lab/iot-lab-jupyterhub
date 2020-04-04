ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub:${JUPYTERHUB_VERSION}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    iproute2 \
    iputils-ping \
    openssh-client \
    wget \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache -r /tmp/requirements.txt && rm -f /tmp/requirements.txt
RUN python3 -m pip install -U --no-cache git+https://github.com/aabadie/cli-tools.git@ssh_key

COPY iotlabauthenticator /src/iotlabauthenticator
RUN python3 -m pip install --no-cache /src/iotlabauthenticator

COPY iotlab_config.py /srv/jupyterhub/iotlab_config.py
RUN mkdir -p /srv/jupyterhub/iotlab_template
COPY templates/login.html /srv/jupyterhub/iotlab_template/login.html

# Download script to automatically stop idle single-user servers
RUN wget https://raw.githubusercontent.com/jupyterhub/jupyterhub/1.1.0/examples/cull-idle/cull_idle_servers.py

# Create user with same uid as the one used in jupyterlab containers
# This ensures the iotlabrc and file .ssh directory have the right ownership.
ARG NB_UID=1000
RUN adduser --disabled-password \
    --gecos "Iotlab user" \
    --uid ${NB_UID} \
    iotlab

RUN mkdir -p /srv/jupyterhub/users
RUN chown ${NB_UID}:users /srv/jupyterhub/users
