from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.0.1'
DESCRIPTION = 'V.I.R.U.S - I\'m the personal assistant of my master abhinand'
LONG_DESCRIPTION = 'V.I.R.U.S - This is created for serving my master Im happy you are lucky to install my package'

# Setting up
setup(
    name="virusai",
    version=VERSION,
    author=" abhinanddreddrive (Red Drive)",
    author_email="<abhi.at.gaming@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'V.I.R.U.S','Smart'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)