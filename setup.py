  #!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.sysconfig import get_python_lib
from setuptools import setup

def readme():
    with open( 'README.md' ) as f:
        return f.read()

setup( name = 'duo3d',
	version = '0.1',
	description = 'DUOSDK python bindings',
	long_description = readme(),
	classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
	keywords = 'duo3d, imu',
	url = 'https://github.com/MateuszOwczarek/python-duo3d',
	author = 'Mateusz Owczarek',
	author_email = 'mateusz.owczarek@dokt.p.lodz.pl',
	license = 'MIT',
	packages = ['duo3d'],
	package_dir = {'duo3d': 'src'},
	data_files = [( get_python_lib(), ["DUOLib.dll"] )],
	include_package_data = True,
	zip_safe = False
 )
