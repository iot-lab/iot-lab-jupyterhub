ARG JUPYTERHUB_VERSION=1.2
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
        unzip \
        vim \
        wget \
        xxd \
        && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Toolchain
ARG ARM_GCC_ARCHIVE='/opt/gcc-arm-none-eabi.tar.bz2'
ARG ARM_GCC_URL='https://developer.arm.com/-/media/Files/downloads/gnu-rm/7-2018q2/gcc-arm-none-eabi-7-2018-q2-update-linux.tar.bz2?revision=bc2c96c0-14b5-4bb4-9f18-bceb4050fee7?product=GNU%20Arm%20Embedded%20Toolchain,64-bit,,Linux,7-2018-q2-update'
RUN mkdir -p /opt && \
    curl -L -o ${ARM_GCC_ARCHIVE} ${ARM_GCC_URL} && \
    echo "299ebd3f1c2c90930d28ab82e5d8d6c0 *${ARM_GCC_ARCHIVE}" | md5sum -c && \
    tar -C /opt -jxf ${ARM_GCC_ARCHIVE} && \
    rm -f ${ARM_GCC_ARCHIVE} && \
    rm -rf /opt/gcc-arm-none-eabi-*/share/doc

ENV PATH ${PATH}:/opt/gcc-arm-none-eabi-7-2018-q2-update/bin

# Python packages
RUN python3 -m pip install --no-cache \
    aiocoap==0.3 \
    asynchttp==0.0.4 \
    asyncssh==2.2.0 \
    azure-iot-device==2.1.1 \
    cbor==1.0.0 \
    ed25519==1.5 \
    iotlabcli==3.2.0 \
    iotlabwscli==0.2.0 \
    ipympl==0.5.6 \
    ipywidgets==7.5.1 \
    jupyterlab==2.0.1 \
    matplotlib==3.2.1 \
    numpy==1.18.2 \
    paho-mqtt==1.5.0 \
    pandas==1.0.3 \
    pycayennelpp==1.3.0 \
    python-cayennelpp==0.0.4 \
    scapy==2.4.3 \
    seaborn==0.10.0 \
    scikit-learn==0.22.2 \
    scipy==1.4.1

# IoT-LAB Plot OML tools
RUN python3 -m pip install -U --no-cache git+https://github.com/iot-lab/oml-plot-tools.git@0.7.0

# Add Jupyterlab interactive extensions
RUN conda install -c conda-forge nodejs
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager --minimize=False
RUN jupyter labextension install jupyter-matplotlib --minimize=False
RUN jupyter nbextension enable --py widgetsnbextension
