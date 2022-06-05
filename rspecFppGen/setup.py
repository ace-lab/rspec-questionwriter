from setuptools import setup 

setup(
    name="rspecFppGen",
    version = "0.1",
    author = "Nelson Lojo",
    author_email = "nelson.lojo@berkeley.edu",
    description = "Generates autograder-friendly formatted files for rspec fpp questions",
    packages = ['.'],
    install_requires=['pyyaml']
)
