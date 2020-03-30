## IoT-LAB JupyterHub


### Testing locally

- Ensure docker-compose is installed. Read
  [the documentation](https://docs.docker.com/compose/install/) for help

- Create a `/tmp/iotlab/users` directory:
  ```
  mkdir -p /tmp/iotlab/users
  ```

- Build the jupyterhub container (from the base directory of this repository):
  ```
  docker build . -t aabadie/iot-lab-training-hub
  ```

- Build the docker image used for the Jupyterlab notebooks:
  ```
  docker build notebooks/. -t aabadie/iot-lab-training-notebooks
  ```

- Create a docker network:
  ```
  docker network create jupyterhub
  ```

- Launch Jupyterhub:
  ```
  docker-compose up
  ```

- Open http://localhost:8000 in a web browser

You can login with an iot-lab account. The .iotlabrc and SSH keys are created
on the fly

**Important:** After the first connection, **on the host computer**, the
ownerhip of the directory containing the users login information
(.iotlabrc and .ssh) must be updated! This is part of future improvements...

```
sudo chown -R 1000:100 /tmp/iotlab/users
```
