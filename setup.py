import re
from setuptools import setup, find_packages

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('ebryx/__init__.py').read(), re.M).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

# setuptools.setup(
#     name='ebcrypto',
#     version='0.1',
#     scripts=['crypto.py'],
#     author="Rana Awais",
#     author_email="rana.awais@ebryx.com",
#     description="A simple utility to encrypt / decrypt text files.",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ]
# )

setup(
    name = "ebryx",
    packages = find_packages(),
    entry_points = {
        "console_scripts": ['ebcrypt = ebryx.crypto.crypto:main'],
    },
    version = version,
    description = "A simple utility to encrypt / decrypt text files.",
    long_description = long_description,
    long_description_content_type="text/markdown",
    author = "Rana Awais",
    author_email = "rana.awais@ebryx.com",
)