import os

c.JupyterHub.template_paths=['.']

# Use IoT-LAB authenticator
c.JupyterHub.authenticator_class = 'iotlabauthenticator.IotlabAuthenticator'

# launch with docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# we need the hub to listen on all ips when it is in a container
c.JupyterHub.hub_ip = '0.0.0.0'
# the hostname/ip that should be used to connect to the hub
# this is usually the hub container's name
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# pick a docker image. This should have the same version of jupyterhub
# in it as our Hub.
c.DockerSpawner.image = 'aabadie/iot-lab-training-notebooks'

# tell the user containers to connect to our docker network
c.DockerSpawner.network_name = 'jupyterhub'

# delete containers when the stop
c.DockerSpawner.remove = True

# Use jupyterlab
c.Spawner.default_url = '/lab'

JUPYTERHUB_DOTSSH_PATH = '/tmp/iotlab/users/{}/.ssh'
JUPYTERHUB_IOTLABRC_PATH = '/tmp/iotlab/users/{}/.iotlabrc'


def spawner_hook(spawner):
    username = spawner.user.name
    iotlabrc_path = JUPYTERHUB_IOTLABRC_PATH.format(username)
    dotssh_path = JUPYTERHUB_DOTSSH_PATH.format(username)

    spawner.environment = {
        'IOTLAB_LOGIN': username
    }

    spawner.volumes = {
        iotlabrc_path: '/home/jovyan/.iotlabrc',
        dotssh_path: '/home/jovyan/.ssh'
    }


c.DockerSpawner.pre_spawn_hook = spawner_hook
