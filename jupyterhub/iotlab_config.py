import os
import sys

# Retrieve useful environment variables
DOCKER_NETWORK_NAME = os.getenv('DOCKER_NETWORK_NAME', 'jupyterhub')
JUPYTERHUB_INSTANCE = os.getenv('JUPYTERHUB_INSTANCE', 'iotlab')
JUPYTERHUB_TRAINING_DIR = os.getenv('JUPYTERHUB_TRAINING_DIR', '/tmp/iot-lab-training')
JUPYTERHUB_HUB_IP = os.getenv('JUPYTERHUB_HUB_IP', '0.0.0.0')
JUPYTERLAB_USERNAME = os.getenv('JUPUTERLAB_USERNAME', 'jovyan')
JUPYTERLAB_DOCKER_IMAGE = os.getenv('JUPYTERLAB_DOCKER_IMAGE',
                                    'aabadie/iot-lab-training-notebooks')
IOTLAB_API_URL = os.getenv('IOTLAB_API_URL', 'https://www.iot-lab.info/api/')
IOTLAB_SITES = os.getenv('IOTLAB_SITES', 'grenoble,saclay')

# General configuration

c.JupyterHub.admin_access = True

# hub listen ips
c.JupyterHub.hub_ip = 'jupyterhub-{}'.format(JUPYTERHUB_INSTANCE)
# hub hostname/ip
c.JupyterHub.hub_connect_ip = 'jupyterhub-{}'.format(JUPYTERHUB_INSTANCE)

# Add path for IoT-LAB custom template
c.JupyterHub.template_paths=['iotlab_template/.']

# Set some limit
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '1G'

# Use IoT-LAB authenticator
if JUPYTERHUB_INSTANCE == 'mooc':
    c.JupyterHub.authenticator_class = 'iotlabauthenticator.IoTLABLTIAuthenticator'
else:
    c.JupyterHub.authenticator_class = 'iotlabauthenticator.IoTLABAuthenticator'
    c.Authenticator.admin_users = {'abadie'}

c.Authenticator.enable_auth_state = True

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

c.DockerSpawner.debug = True

# Ensure the user containers are removed after 1h of inactivity
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python3 /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
    {
        'name': 'password',
        'url': 'http://127.0.0.1:10101',
        'command': [sys.executable, '/srv/jupyterhub/services/password/password.py'],
        'environment': {
            'JUPYTERHUB_CRYPT_KEY': os.environ['JUPYTERHUB_CRYPT_KEY']
        }
    }
]

WORK_DIR =  '/home/{}/work'.format(JUPYTERLAB_USERNAME)

volume_name_template = 'jupyterhub-user-{username}'
if JUPYTERHUB_INSTANCE == 'mooc':
    volume_name_template = 'jupyterhub-user-mooc-{username}'

c.DockerSpawner.volumes = {
    JUPYTERHUB_TRAINING_DIR: '/opt/training',
    volume_name_template: WORK_DIR,
}


def userdata_hook(spawner, auth_state):
    spawner.userdata = auth_state["userdata"]


c.Spawner.auth_state_hook = userdata_hook


# Customize the user container just before it starts
def spawner_hook(spawner):
    """Add some custom logic just before launching the user container"""

    spawner.environment = {
        'AUTHENTICATOR': spawner.userdata['authenticator'],
        'IOTLAB_LOGIN': spawner.userdata['username'],
        'IOTLAB_PASSWORD': spawner.userdata['password'],
        'IOTLAB_API_URL': IOTLAB_API_URL,
        'IOTLAB_SITES': IOTLAB_SITES,
    }

    # Directly jump in the training directory
    spawner.notebook_dir = '{}/training'.format(WORK_DIR)


c.DockerSpawner.pre_spawn_hook = spawner_hook

# Fix for GDB and RIOT native
c.DockerSpawner.extra_host_config = {"cap_add": "SYS_PTRACE", "security_opt": ["seccomp=unconfined"]}
