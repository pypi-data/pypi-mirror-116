from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Dates Handler - simple method for date manipulation'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="dateHandler", 
        version=VERSION,
        author="Alexandre Suire",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['arrow'],
        keywords=['python', 'dates'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)