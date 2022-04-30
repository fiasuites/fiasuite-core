
   
from setuptools import setup

setup(
    name="fiasuite",
    version="1.0.0",
    author="Solomon ABOYEJI",
    author_email="solomon@regnify.com",
    packages=[
        "app/services",
    ],
    description="FiaSuite HTTP Application",
    long_description=open("README.md").read(),
    install_requires=open("requirements.txt").read().split("\n"),
)