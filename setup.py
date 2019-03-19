import re
from setuptools import setup, find_packages


version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('ebryx/__init__.py').read(), re.M).group(1)


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='ebryx',
    packages=['crypto'],
    entry_points={
        'console_scripts': ['ebcrypt = ebryx.crypto._crypto:main'],
    },
    version=version,
    description='A simple utility to encrypt / decrypt text files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rana Awais',
    author_email='rana.awais@ebryx.com',
    install_requires=['cryptography'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
