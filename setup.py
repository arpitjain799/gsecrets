from setuptools import setup, find_packages
import os

setup(name='gsecrets',
      version='1.0.0',
      description='API and CLI for securely managing secrets',
      url='https://github.com/openeemeter/gsecrets',
      author='Open Energy Efficiency',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
          'gsecrets = gsecrets.cli:cli',
        ]
      },
      install_requires=[
        'click',
        'ndg-httpsclient',
        'pyasn1',
        'pyopenssl',
        'requests',
      ],
)