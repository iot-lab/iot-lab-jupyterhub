import os

# Retrieve useful environment variables
DOCKER_NETWORK_NAME = os.getenv('DOCKER_NETWORK_NAME', 'jupyterhub')
JUPYTERHUB_USERS_DIR = os.getenv('JUPYTERHUB_USERS_DIR', '/tmp/users')
JUPYTERHUB_HUB_IP = os.getenv('JUPYTERHUB_HUB_IP', '0.0.0.0')
JUPYTERLAB_USERNAME = os.getenv('JUPUTERLAB_USERNAME', 'jovyan')
JUPYTERLAB_DOCKER_IMAGE = os.getenv('JUPYTERLAB_DOCKER_IMAGE',
                                    'aabadie/iot-lab-training-notebooks')

# General configuration

# hub listen ips
c.JupyterHub.hub_ip = 'jupyterhub'
# hub hostname/ip
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# Add path for IoT-LAB custom template
c.JupyterHub.template_paths=['iotlab_template/.']

# Set some limit
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '2G'

# Use IoT-LAB authenticator
c.JupyterHub.authenticator_class = 'iotlabauthenticator.IotlabAuthenticator'

# Use Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Authenticator configuration

c.Authenticator.admin_users = {'abadie'}

# Docker spawner configuration

c.DockerSpawner.image = JUPYTERLAB_DOCKER_IMAGE

# tell the user containers to connect to our docker network
c.DockerSpawner.network_name = DOCKER_NETWORK_NAME

# delete containers when they are stopped
c.DockerSpawner.remove = True

# Use jupyterlab by default
c.Spawner.default_url = '/lab'

# Directly jump in the training directory
c.DockerSpawner.notebook_dir = '~/work/training'

c.DockerSpawner.debug = True

# Ensure the user containers are removed after 1h of inactivity
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python3 /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]

IOTLABRC_PATH = os.path.join(JUPYTERHUB_USERS_DIR, '{username}', '.iotlabrc')
DOTSSH_PATH = os.path.join(JUPYTERHUB_USERS_DIR, '{username}', '.ssh')
WORK_PATH = os.path.join(JUPYTERHUB_USERS_DIR, '{username}', 'work')

c.DockerSpawner.volumes = {
    IOTLABRC_PATH: '/home/{}/.iotlabrc'.format(JUPYTERLAB_USERNAME),
    DOTSSH_PATH: '/home/{}/.ssh'.format(JUPYTERLAB_USERNAME),
    WORK_PATH: '/home/{}/work'.format(JUPYTERLAB_USERNAME)
}


# Customize the user container just before it starts
def spawner_hook(spawner):
    """Add some custom logic just before launching the user container"""
    username = spawner.user.name

    spawner.environment = {
        'IOTLAB_LOGIN': username
    }


c.DockerSpawner.pre_spawn_hook = spawner_hook

# Fix for GDB and RIOT native
c.DockerSpawner.extra_host_config = {"cap_add": "SYS_PTRACE", "security_opt": ["seccomp=unconfined"]}
