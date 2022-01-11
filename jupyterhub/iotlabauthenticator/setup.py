from setuptools import setup

setup(
    name='iotlabauthenticator',
    version='0.1',
    description='IoT-LAB Authenticators for JupyterHub',
    url='https://github.com/iot-lab/iot-lab-hub',
    author='IoT-LAB developers',
    author_email='admin@iot-lab.info',
    license='3 Clause BSD',
    packages=['iotlabauthenticator'],
    entry_points={
        'jupyterhub.authenticators': [
            'iotlabauthenticator = iotlabauthenticator:IoTLABAuthenticator',
            'iotlabltiauthenticator = iotlabauthenticator:IoTLABLTIAuthenticator',
        ],
    },
    install_requires=[
        "jupyterhub-ltiauthenticator==1.1",
    ],
)
