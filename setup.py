# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in swiss_factur_x_e_invoicing/__init__.py
from swiss_factur_x_e_invoicing import __version__ as version

setup(
	name='swiss_factur_x_e_invoicing',
	version=version,
	description='A E-Invoice PDF Creation library',
	author='Grynn',
	author_email='grynn@in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
