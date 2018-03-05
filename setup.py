from setuptools import setup

__version__ = '0.0.1'
__author__ = 'Daniel Eidan'

requirements = [
    # 'selenium==2.53.6',
    'selenium==3.9.0',
    'clarifai==2.0.8',
    'pyvirtualdisplay',
    'emoji'
]

description = 'Instagram Helper'

setup(
    name='little-helper',
    version=__version__,
    author=__author__,
    author_email='daniel.eidan@gmail.com',
    url='https://github.com/DanielEidan/little-helper',
    py_modules='little-helper',
    description=description,
    install_requires=requirements)


# python setup.py install