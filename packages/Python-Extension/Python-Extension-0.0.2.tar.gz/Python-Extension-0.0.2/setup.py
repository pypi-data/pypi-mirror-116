from setuptools import *

setup(
    name = 'Python-Extension',
    version = '0.0.2',
    description = 'Python Extension ( For Python 3.10 or more later )',
    license = 'GPL',
    author = 'Yile Wang',
    packages = find_packages(),
    python_requires = '>=3.10',
    include_package_data = True
    )
