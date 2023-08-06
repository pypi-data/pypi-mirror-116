
import pathlib
from setuptools import setup, find_packages

install_requires = [
	'numpy',
	'pandas'
]

setup(name = "textprocessinglib",
	version = "0.0.1",
	author = "Key Tai",
	author_email = "taihongwenkey@gmail.com",
	description = "Testing creation of package",
	long_description=open("README.md", "r", encoding="utf-8").read(),
    	long_description_content_type="text/markdown",
	license = "Apache",
	install_requires = install_requires,
	packages=find_packages()
)
