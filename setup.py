#!/usr/bin/env python

import codecs
import os

from setuptools import find_packages
from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

install_requires = [
    "kubernetes==29.0.0",
    "configargparse",
    "hera_utils==0.2.0",
]
dependency_links = [
    "git+https://github.com/VCityTeam/hera_utils.git#egg=hera_utils-0.2.0"
]

version = None
exec(open("hera_k8s_utils/version.py").read())

long_description = ""
with codecs.open("./README.md", encoding="utf-8") as readme_md:
    long_description = readme_md.read()

setup(
    name="hera_k8s_utils",
    version=version,
    description="K8s helpers for Hera (workflows) usage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VCityTeam/ExpeData-Workflows_testing/hera_utils",
    project_urls={
        "Source": "https://github.com/VCityTeam/hera_k8s_utils",
        "Tracker": "https://github.com/VCityTeam/hera_k8s_utils",
    },
    packages=find_packages(exclude=["tests.*", "tests"]),
    python_requires=">=3.10",
    install_requires=install_requires,
    dependency_links=dependency_links,
    zip_safe=False,
    classifiers=[
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    maintainer="vcity_devel",
    maintainer_email="vcity@liris.cnrs.fr",
)
