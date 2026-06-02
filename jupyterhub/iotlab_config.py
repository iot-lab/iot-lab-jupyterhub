import os
import sys

from docker.types import LogConfig

# Retrieve useful environment variables
DOCKER_NETWORK_NAME = os.getenv("DOCKER_NETWORK_NAME", "jupyterhub")
JUPYTERHUB_TRAINING_DIR = os.getenv("JUPYTERHUB_TRAINING_DIR", "/tmp/iot-lab-training")
JUPYTERHUB_HUB_IP = os.getenv("JUPYTERHUB_HUB_IP", "0.0.0.0")
JUPYTERLAB_USERNAME = os.getenv("JUPUTERLAB_USERNAME", "jovyan")
JUPYTERLAB_DOCKER_IMAGE = os.getenv(
    "JUPYTERLAB_DOCKER_IMAGE", "aabadie/iot-lab-training-notebooks"
)
IOTLAB_USE_CUSTOM_API_URL = bool(os.getenv("IOTLAB_API_URL", 0))
IOTLAB_API_URL = os.getenv("IOTLAB_API_URL", "https://www.iot-lab.info/api/")
IOTLAB_SITES = os.getenv("IOTLAB_SITES", "grenoble,saclay")

# General configuration
c.JupyterHub.base_url = "/"

# hub listen ips
c.JupyterHub.hub_ip = "jupyterhub-iotlab"
# hub hostname/ip
c.JupyterHub.hub_connect_ip = "jupyterhub-iotlab"

# Add path for IoT-LAB custom template
c.JupyterHub.template_paths = ["iotlab_template/."]

# Use IoT-LAB authenticator
c.JupyterHub.authenticator_class = "iotlabauthenticator"
c.Authenticator.allow_all = True
c.Authenticator.admin_users = {"abadie"}

c.Authenticator.enable_auth_state = True

# Use Docker spawner
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Docker spawner configuration

# Set some limit
c.DockerSpawner.cpu_limit = 1
c.DockerSpawner.mem_limit = "2G"

# Docker image spawned
c.DockerSpawner.image = JUPYTERLAB_DOCKER_IMAGE

# tell the user containers to connect to our docker network
c.DockerSpawner.network_name = DOCKER_NETWORK_NAME

# delete containers when they are stopped
c.DockerSpawner.remove = True

# Use jupyterlab by default
c.Spawner.default_url = "/lab"

c.DockerSpawner.debug = True

# Ensure the user containers are removed after 1h of inactivity
c.JupyterHub.services = [
    {
        "name": "idle-culler",
        "command": [sys.executable, "-m", "jupyterhub_idle_culler", "--timeout=3600"],
    },
]

c.JupyterHub.load_roles = [
    {
        "name": "idle-culler",
        "services": [
            "idle-culler",
        ],
        "scopes": [
            "list:users",
            "read:users:activity",
            "admin:servers",
        ],
    },
]

WORK_DIR = "/home/{}/work".format(JUPYTERLAB_USERNAME)

c.DockerSpawner.volumes = {
    JUPYTERHUB_TRAINING_DIR: "/opt/training",
    "jupyterhub-user-{username}": WORK_DIR,
}


def userdata_hook(spawner, auth_state):
    spawner.userdata = auth_state["userdata"]


c.Spawner.auth_state_hook = userdata_hook


# Customize the user container just before it starts
def spawner_hook(spawner):
    """Add some custom logic just before launching the user container"""

    spawner.environment = {
        "IOTLAB_LOGIN": spawner.userdata["username"],
        "IOTLAB_PASSWORD": spawner.userdata["password"],
        "IOTLAB_SITES": IOTLAB_SITES,
    }
    if IOTLAB_USE_CUSTOM_API_URL is True:
        spawner.environment.update({"IOTLAB_API_URL": IOTLAB_API_URL})

    # Directly jump in the training directory
    spawner.notebook_dir = "{}/training".format(WORK_DIR)

    log_config = LogConfig(
        type=LogConfig.types.SYSLOG,
        config={"tag": "jupyterhub-user-{}".format(spawner.userdata["username"])},
    )
    spawner.extra_host_config.update({"log_config": log_config})


c.DockerSpawner.pre_spawn_hook = spawner_hook

# Fix for GDB and RIOT native
c.DockerSpawner.extra_host_config = {
    "cap_add": "SYS_PTRACE",
    "security_opt": ["seccomp=unconfined"],
}
