# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as file_handler:
    requirements = file_handler.readlines()

setup(
    name='cicloguia',
    version='0.0.1',
    install_requires=requirements,
    packages=find_packages(include=["src", "src.*"]),
    author='Sebastian Lopez Norambuena',
    author_email='seblopezn@gmail.com',
    python_requires='>=3.8',
)
