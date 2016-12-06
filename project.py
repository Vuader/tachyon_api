import os
import sys
from setuptools import find_packages

config = {
        "name": "tachyon-auth",
        "author": "Christiaan F Rademan, Dave Kruger",
        "author_email": "tachyon@fwiw.co.za",
        "description": "Tachyon - Authentication Modules",
        "license": "BSD 3-Clause",
        "keywords": "tachyon authentication",
        "url": "https://github.com/vision1983/tachyon_auth",
        "packages": find_packages(),
        "namespace_packages": [
            'tachyon'
            ],
        "classifiers": [
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Environment :: Other Environment",
            "Intended Audience :: Information Technology",
            "Intended Audience :: System Administrators",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7"
            ]
        }

