FROM fitiotlab/iot-lab-jupyterlab-base

WORKDIR ${HOME}/work

RUN echo "cd ~/work/training" >> ${HOME}/.bashrc

RUN chown -R ${NB_UID} ${HOME}

# Custom javascript to customize jupyter style for Fun users
COPY custom /opt/custom_jupyter

# Custom startup script
COPY entrypoint.sh /srv/entrypoint.sh
RUN chmod +x /srv/entrypoint.sh
ENTRYPOINT ["tini", "--", "/srv/entrypoint.sh"]
CMD ["start-singleuser.sh"]

# Run as jovyan (default user)
USER ${NB_USER}
