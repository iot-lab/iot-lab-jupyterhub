ARG JUPYTERHUB_VERSION=1.5
FROM jupyterhub/singleuser:${JUPYTERHUB_VERSION}

LABEL maintainer="alexandre.abadie@inria.fr"

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bsdmainutils \
        build-essential \
        ca-certificates \
        curl \
        git \
        g++-multilib \
        iproute2 \
        iputils-ping \
        mosquitto-clients \
        net-tools \
        openssh-client \
        socat \
        texlive-fonts-recommended \
        texlive-latex-recommended \
        texlive-plain-generic \
        texlive-xetex \
        unzip \
        vim \
        wget \
        xxd \
        && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ARM Toolchain
ARG ARM_URLBASE=https://developer.arm.com/-/media/Files/downloads/gnu-rm
ARG ARM_URL=${ARM_URLBASE}/9-2019q4/gcc-arm-none-eabi-9-2019-q4-major-x86_64-linux.tar.bz2
ARG ARM_MD5=fe0029de4f4ec43cf7008944e34ff8cc
ARG ARM_FOLDER=gcc-arm-none-eabi-9-2019-q4-major
RUN mkdir -p /opt && \
    curl -L -o /opt/gcc-arm-none-eabi.tar.bz2 ${ARM_URL} && \
    echo "${ARM_MD5} /opt/gcc-arm-none-eabi.tar.bz2" | md5sum -c && \
    tar -C /opt -jxf /opt/gcc-arm-none-eabi.tar.bz2 && \
    rm -f /opt/gcc-arm-none-eabi.tar.bz2 && \
    rm -rf /opt/gcc-arm-none-eabi-*/share/doc

ENV PATH ${PATH}:/opt/${ARM_FOLDER}/bin

# Arm GCC 5 for contiki-ng
ARG ARM_GCC_ARCHIVE='/opt/gcc-arm-none-eabi-5.tar.bz2'
ARG ARM_GCC_URL='https://launchpad.net/gcc-arm-embedded/5.0/5-2015-q4-major/+download/gcc-arm-none-eabi-5_2-2015q4-20151219-linux.tar.bz2'
RUN mkdir -p /opt && \
    curl -L -o ${ARM_GCC_ARCHIVE} ${ARM_GCC_URL} && \
    echo "f88caac80b4444a17344f57ccb760b90 *${ARM_GCC_ARCHIVE}" | md5sum -c && \
    tar -C /opt -jxf ${ARM_GCC_ARCHIVE} && \
    rm -f ${ARM_GCC_ARCHIVE} && \
    rm -rf /opt/gcc-arm-none-eabi-*/share/doc

# Python packages
RUN python3 -m pip install --no-cache \
    aiocoap==0.4.3 \
    asynchttp==0.0.4 \
    asyncssh==2.2.0 \
    azure-iot-device==2.1.1 \
    cbor==1.0.0 \
    cbor2==5.4.2 \
    cryptography==36.0.0 \
    ed25519==1.5 \
    iotlabcli==3.3.0 \
    iotlabwscli==0.2.0 \
    ipympl==0.8.5 \
    ipywidgets==7.6.5 \
    jupyterlab==3.2.6 \
    matplotlib==3.5.1 \
    numpy==1.22.0 \
    oml-plot-tools==0.8.0 \
    paho-mqtt==1.6.1 \
    pandas==1.3.5 \
    pycayennelpp==2.4.0 \
    python-cayennelpp==0.0.4 \
    scapy==2.4.5 \
    seaborn==0.11.2 \
    scikit-learn==1.0.2 \
    scipy==1.7.3

# Add Jupyterlab interactive extensions
RUN conda update -n base conda
RUN conda install -c conda-forge nodejs
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager --minimize=False
RUN jupyter labextension install jupyter-matplotlib --minimize=False
RUN jupyter nbextension enable --py widgetsnbextension

# Don't show conda env in prompt by default
RUN conda config --set changeps1 False
