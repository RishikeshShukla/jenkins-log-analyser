from distutils.core import setup
from setuptools import find_packages

with open('requirments.txt', 'r') as f:
    required = f.read().splitlines()

setup(
    name="jenkins-log-analyser",
    version="1.0.1",
    description="Jenkins-Log-Analyser",
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python::3.6',
        "Operating System :: OS Independent",
    ]
)
