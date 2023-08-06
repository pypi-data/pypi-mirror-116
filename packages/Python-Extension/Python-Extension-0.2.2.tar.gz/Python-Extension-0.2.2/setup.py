from setuptools import *

setup(
    name = 'Python-Extension',
    version = '0.2.2',
    description = 'Python Extension Function',
    license = 'GPL',
    author = 'Yile Wang',
    packages = find_packages(),
    python_requires = '>=3.10',
    include_package_data = True
    )
