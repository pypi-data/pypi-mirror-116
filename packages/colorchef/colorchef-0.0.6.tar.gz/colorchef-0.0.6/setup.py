from setuptools import setup, find_packages
from os import path

VERSION = '0.0.6' 
DESCRIPTION = 'Paint your terminal with beautifull colors.'
# LONG_DESCRIPTION = 'This package lets you print colored text on the terminal.'
# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
# Setting up
setup(
       # the name must match the folder name 'colorchef'
        name="colorchef", 
        version=VERSION,
        author="Mithilesh Pradhan",
        author_email="knowmit@gmail.com",
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package.
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Information Technology",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)