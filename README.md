## IoT-LAB JupyterHub


### Testing locally

- Ensure docker-compose is installed. Read
  [the documentation](https://docs.docker.com/compose/install/) for help

- Create a `/tmp/iotlab/users` directory:
  ```
  mkdir -p /tmp/iotlab/users
  ```

- Clone iot-lab-training in the `/tmp/iotlab/users` directory:
  ```
  git clone https://github.com/iot-lab/iot-lab-training /tmp/iotlab/users/.training
  ```

- Build the images for jupyterhub and jupyterlab:
  ```
  docker-compose build
  ```

- Create a docker network:
  ```
  docker network create iotlab
  ```

- Launch Jupyterhub:
  ```
  docker-compose up
  ```

- Open http://localhost:8000 in a web browser

You can login with an iot-lab account. The .iotlabrc and SSH keys are created
on the fly
