# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

version = '1.0.0'

setup(name='ge.ibis.etl',
      version=version,
      description='IBIS ETL',
      url='',
      author='Julien Stegle',
      author_email='julien.stegle@ge.com',
      license='Proprietary',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Programming Language :: Python :: 3.5',
          'Intended Audience :: Healthcare Industry',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Operating System :: OS Independent',
          'License :: Other/Proprietary License',
      ],
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ge', 'ge.ibis'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'pymysql==0.7.11',
          'pymongo==3.4',
          'requests==2.18.4',
          'python-dateutil==2.7.2',
          'ge.ibis.entities'
      ],
      extras_require={
          # 'test': ['mockito==1.0.12'],
      },)
