ARG JUPYTERHUB_VERSION=5
FROM quay.io/jupyterhub/singleuser:${JUPYTERHUB_VERSION}

LABEL maintainer="alexandre.abadie@inria.fr"

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bsdmainutils \
        build-essential \
        ca-certificates \
        clang \
        curl \
        git \
        g++-multilib \
        iproute2 \
        iputils-ping \
        make \
        mosquitto-clients \
        net-tools \
        ninja-build \
        openssh-client \
        pkg-config \
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
ARG ARM_URLBASE=https://developer.arm.com/-/media/Files/downloads/gnu
ARG ARM_URL=${ARM_URLBASE}/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi.tar.xz
ARG ARM_SHA256=62a63b981fe391a9cbad7ef51b17e49aeaa3e7b0d029b36ca1e9c3b2a9b78823
ARG ARM_FOLDER=arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi
RUN mkdir -p /opt && \
    curl -L -o /opt/gcc-arm-none-eabi.tar.xz ${ARM_URL} && \
    echo "${ARM_SHA256}  /opt/gcc-arm-none-eabi.tar.xz" | sha256sum -c && \
    tar -C /opt -xf /opt/gcc-arm-none-eabi.tar.xz && \
    rm -f /opt/gcc-arm-none-eabi.tar.xz && \
    rm -rf /opt/${ARM_FOLDER}/share/doc

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

# Rust toolchain with ARM embedded targets
USER jovyan
ENV PATH=/home/jovyan/.cargo/bin:${PATH}
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --no-modify-path --profile minimal --default-toolchain stable && \
    rustup target add \
        thumbv6m-none-eabi \
        thumbv7m-none-eabi \
        thumbv7em-none-eabi \
        thumbv7em-none-eabihf \
        thumbv8m.base-none-eabi \
        thumbv8m.main-none-eabi \
        thumbv8m.main-none-eabihf && \
    rm -rf /home/jovyan/.cargo/registry /home/jovyan/.cargo/git
# Install laze, a build system for embedded Rust projects that can speed up compilation by caching build artifacts
RUN cargo install laze
USER root

# Python packages
RUN python3 -m pip install --no-cache \
    aiocoap==0.4.17 \
    asynchttp==0.0.4 \
    asyncssh==2.23.0 \
    cbor==1.0.0 \
    cbor2==6.1.1 \
    cryptography==48.0.0 \
    git+https://github.com/iot-lab/cli-tools.git@master \
    git+https://github.com/iot-lab/ws-cli-tools.git@master \
    ipympl==0.10.0 \
    ipywidgets==8.1.8 \
    jupyterlab==4.5.7 \
    matplotlib==3.10.9 \
    numpy==2.4.6 \
    git+https://github.com/iot-lab/oml-plot-tools.git@master \
    paho-mqtt==2.1.0 \
    pandas==3.0.3 \
    pycayennelpp==2.4.0 \
    python-cayennelpp==0.1.0 \
    scapy==2.7.0 \
    seaborn==0.13.2 \
    scikit-learn==1.8.0 \
    scipy==1.17.1

# JupyterLab 4.x: extensions are distributed as pip packages with prebuilt assets
RUN python3 -m pip install --no-cache jupyterlab-widgets jupytext jupyter_contrib_nbextensions

# Set markdown files to open as Jupytext notebooks by default
RUN mkdir -p /opt/conda/share/jupyter/lab/settings && \
    echo '{"@jupyterlab/docmanager-extension:plugin": {"defaultViewers": {"markdown": "Jupytext Notebook"}}}' \
    > /opt/conda/share/jupyter/lab/settings/overrides.json

# Don't show conda env in prompt by default
RUN conda config --set changeps1 False
