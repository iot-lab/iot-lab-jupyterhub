import os

# Retrieve useful environment variables
DOCKER_NETWORK_NAME = os.getenv('DOCKER_NETWORK_NAME', 'jupyterhub')
JUPYTERHUB_USERS_DIR = os.getenv('JUPUTERHUB_USERS_DIR', '/tmp/iotlab/users/')
JUPYTERLAB_USERNAME = os.getenv('JUPUTERLAB_USERNAME', 'jovyan')
JUPYTERLAB_DOCKER_IMAGE = os.getenv('JUPYTERLAB_DOCKER_IMAGE',
                                    'aabadie/iot-lab-training-notebooks')
JUPYTERHUB_HUB_IP = os.getenv('JUPYTERHUB_HUB_IP', '0.0.0.0')

# General configuration

# hub listen ips
c.JupyterHub.hub_ip = JUPYTERHUB_HUB_IP
# hub hostname/ip
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# Add path for IoT-LAB custom template
c.JupyterHub.template_paths=['iotlab_template/.']

# Use IoT-LAB authenticator
c.JupyterHub.authenticator_class = 'iotlabauthenticator.IotlabAuthenticator'

# Use Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'


# Docker spawner configuration

c.DockerSpawner.image = JUPYTERLAB_DOCKER_IMAGE

# tell the user containers to connect to our docker network
c.DockerSpawner.network_name = DOCKER_NETWORK_NAME

# delete containers when they are stopped
c.DockerSpawner.remove = True

# Use jupyterlab by default
c.Spawner.default_url = '/lab'

# Ensure the user containers are removed after 1h of inactivity
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python3 /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]

# Customize the user container just before it starts
def spawner_hook(spawner):
    """Add some custom logic just before launching the user container"""
    username = spawner.user.name
    iotlabrc_path = os.path.join(JUPYTERHUB_USERS_DIR, username, '.iotlabrc')
    dotssh_path = os.path.join(JUPYTERHUB_USERS_DIR, username, '.ssh')

    spawner.environment = {
        'IOTLAB_LOGIN': username
    }

    spawner.volumes = {
        iotlabrc_path: '/home/{}/.iotlabrc'.format(JUPYTERLAB_USERNAME),
        dotssh_path: '/home/{}/.ssh'.format(JUPYTERLAB_USERNAME)
    }


c.DockerSpawner.pre_spawn_hook = spawner_hook
