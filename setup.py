from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='api',
      version="1.0",
      description="This is a project developed by students to bridge information data gaps that are seen across the Brazilian coast. We have gathered data from various buoys to create one host where the information is available to the public.",
      packages=find_packages(),
      install_requires=requirements,
      test_suite='tests',
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
