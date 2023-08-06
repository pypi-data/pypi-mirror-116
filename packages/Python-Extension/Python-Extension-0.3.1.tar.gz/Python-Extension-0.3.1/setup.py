from setuptools import *

setup(
    name = 'Python-Extension',
    version = '0.3.1',
    description = 'Python Extension Function',
    license = 'GPL',
    author = 'Yile Wang',
    packages = find_packages(),
    python_requires = '>=3.10',
    include_package_data = True
    )
