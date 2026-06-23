#!/bin/bash

set -e

: ${IOTLAB_SITES:=grenoble,lille,saclay,strasbourg}

# If the run command is the default, do some initialization first
if [ "$(which "$1")" = "/usr/local/bin/start-singleuser.sh" ]
then
    : ${NOTEBOOK_DIR:=/home/${NB_USER}/work}

    # SSH key setup must complete before JupyterLab starts (symlink is needed)
    if [ ! -f /home/${NB_USER}/work/.ssh/id_rsa ]
    then
        mkdir -p /home/${NB_USER}/work/.ssh
        echo "Create SSH keys and init account"
        ssh-keygen -t rsa -q -N "" -C jupyterhub@iotlab -f /home/${NB_USER}/work/.ssh/id_rsa
    else
        echo "SSH key already exists"
    fi
    ln -sf /home/${NB_USER}/work/.ssh /home/${NB_USER}/.ssh

    # The training directory must exist before JupyterLab starts because it is
    # used as the server root_dir, so bootstrap it synchronously here.
    if [ ! -d /home/${NB_USER}/work/training ]
    then
        echo "Bootstraping training directory for user '${IOTLAB_LOGIN}'"
        cp -R /opt/training /home/${NB_USER}/work/training
    else
        echo "Training directory already exists"
    fi

    # Run slow network operations in the background so JupyterLab can start
    # immediately without waiting for them.
    (
        iotlab-auth --user="${IOTLAB_LOGIN}" --password="${IOTLAB_PASSWORD}" --add-ssh-key
        echo "Configure IoT-LAB access on $(echo ${IOTLAB_SITES} | sed -e s'/,/, /g') sites"
        for site in $(echo ${IOTLAB_SITES} | tr , ' ')
        do
            scp -o "ConnectTimeout 3" -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" /home/${NB_USER}/.iotlabrc ${IOTLAB_LOGIN}@${site}.iot-lab.info:.iotlabrc || echo "Cannot connect to ${site}";
        done
    ) &

fi

# Only configure labextensions once; the config is written to the persistent
# user volume so there is no need to repeat this on every container start.
_LABEXT_FLAG=/home/${NB_USER}/work/.labext_configured
if [ ! -f "${_LABEXT_FLAG}" ]
then
    jupyter labextension enable jupyterlab_jupytext
    jupyter labextension disable "@jupyterlab/apputils-extension:announcements"
    touch "${_LABEXT_FLAG}"
fi

echo "All done, starting jupyterlab..."
# Run the command provided
exec "$@"
