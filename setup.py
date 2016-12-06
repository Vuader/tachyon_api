import os
import subprocess

from setuptools import setup

try:
    import project
except Exception as e:
    raise Exception("Missing or Broken Configuration" +
                    " project.py file (%s)" % (e,))

if hasattr(project, 'config'):
    if isinstance(project.config, dict):
        config = project.config
    else:
        raise Exception("'project.config' object not" +
                        " dictionary in project.py file.")
else:
    raise Exception("Missing config dictionary in project.py file.")

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as x:
    requirements = x.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as x:
    readme = x.read()

version_py = os.path.join(os.path.dirname(__file__), 'version.py')
if os.path.isfile(version_py):
    with open(version_py, 'r') as fh:
        version_git = open(version_py).read()
        version_git = version_git.strip()
        version_git = version_git.split('=')[-1]
        version_git = version_git.replace('\'', '')
else:
    version_git = '0.0.0'

print("%s %s\n" % (config['name'], version_git))

setup(
    install_requires=requirements,
    long_description=readme,
    version=version_git,
    **config
)
