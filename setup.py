from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in hana_amt_credit/__init__.py
from hana_amt_credit import __version__ as version

setup(
	name="hana_amt_credit",
	version=version,
	description="HanaAMT Credit info",
	author="John",
	author_email="yuntan0@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
