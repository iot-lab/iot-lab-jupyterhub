#!/bin/bash

set -e

SITES="lille lyon grenoble saclay strasbourg"
if [[ ${IOTLAB_API_URL} == "https://devwww.iot-lab.info/api/" ]]
then
    SITES="devgrenoble devsaclay"
fi

# If the run command is the default, do some initialization first
if [ "$(which "$1")" = "/usr/local/bin/start-singleuser.sh" ]
then
    # Clone sample notebooks to user's notebook directory.  Assume $NB_USER's work
    # directory if notebook directory not explicitly set.  `git clone` will fail
    # if target directory already exists and is not empty, which likely means
    # that we've already done it, so just ignore.
    : ${NOTEBOOK_DIR:=/home/${NB_USER}/work}
    if [ ! -f /home/${NB_USER}/work/.ssh/id_rsa ]
    then
        mkdir -p /home/${NB_USER}/work/.ssh
        echo "Create SSH keys and init account"
        ssh-keygen -t rsa -q -N "" -C jupyterhub@iotlab -f /home/${NB_USER}/work/.ssh/id_rsa
    else
        echo "SSH key already exists"
    fi
    ln -sf /home/${NB_USER}/work/.ssh /home/${NB_USER}/.ssh
    iotlab-auth -u ${IOTLAB_LOGIN} -p ${IOTLAB_PASSWORD} --add-ssh-key
    for site in ${SITES}
    do
        scp -o "ConnectTimeout 3" -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" /home/${NB_USER}/.iotlabrc ${IOTLAB_LOGIN}@${site}.iot-lab.info:.iotlabrc || echo "Error connecting to ${site}";
    done

    if [ ! -d /home/${NB_USER}/work/training ]
    then
        cp -R /opt/training /home/${NB_USER}/work/training
    else
        echo "Training directory already exists"
    fi

    if [[ ${AUTHENTICATOR} == "mooc" ]]
    then
        echo "Configure custom jupyter for Mooc"
        cp -R /opt/custom_jupyter /home/${NB_USER}/.jupyter/custom
    else
        echo "Regular IoT-LAB user"
    fi
fi

# Run the command provided
exec "$@"
