FROM fitiotlab/iot-lab-jupyterlab-base

WORKDIR ${HOME}/work

RUN echo "cd ~/work/training" >> ${HOME}/.bashrc

RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}
