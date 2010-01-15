from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='django-localflavor-sl',
      version=version,
      description="Slovenian Django localflavor",
      long_description=open('README').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Gasper Zejn',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=[
        "Django",
      ],
      )
