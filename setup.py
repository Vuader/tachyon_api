import os

try:
    from setuptools import setup
    from setuptools import find_packages
except Exception as e:
    print("Requires 'setuptools'")
    print(" pip install setuptools")
    exit()

config = {
    "name": "tachyon-api",
    "author": "Christiaan F Rademan, Dave Kruger",
    "author_email": "tachyon@fwiw.co.za",
    "description": "Tachyon - API Inteface Modules",
    "license": "BSD 3-Clause",
    "keywords": "tachyon api",
    "url": "https://github.com/vision1983/tachyon_api",
    "packages": find_packages(),
    "include_package_data": True,
    "package_data": {'': ['requirements.txt']},
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

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if os.path.exists(os.path.join(os.path.dirname(__file__),
                               'requirements.txt')):
    with open(os.path.join(os.path.dirname(__file__),
                           'requirements.txt')) as x:
        requirements = x.read().splitlines()
else:
    requirements = []

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as x:
    readme = x.read()

version_py = os.path.join(os.path.dirname(__file__), 'tachyon/api/version.py')
if os.path.isfile(version_py):
    with open(version_py, 'r') as fh:
        version_git = open(version_py).read()
        version_git = version_git.strip()
        version_git = version_git.split('=')[-1]
        version_git = version_git.replace('\'', '')
else:
    version_git = '0.0.0'

setup(
    install_requires=requirements,
    long_description=readme,
    version=version_git,
    **config
)
