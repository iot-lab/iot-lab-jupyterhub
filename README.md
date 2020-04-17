## IoT-LAB JupyterHub


### Testing locally

- Ensure docker-compose is installed. Read
  [the documentation](https://docs.docker.com/compose/install/) for help

- Clone iot-lab-training in `/tmp`:
  ```
  git clone --recurse-submodules https://github.com/iot-lab/iot-lab-training /tmp/iot-lab-training
  ```

- Launch Jupyterhub:
  ```
  docker-compose up
  ```

- Open http://localhost:8000 in a web browser

You can login with an iot-lab account. The .iotlabrc and SSH keys are created
on the fly
