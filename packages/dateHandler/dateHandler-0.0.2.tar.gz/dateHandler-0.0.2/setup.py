from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Dates Handler - simple method for date manipulation'
LONG_DESCRIPTION = 'This package aims to facilitate date processing in Python for unexperimented users. It is based on the Arrow library (https://arrow.readthedocs.io/en/latest/)'

# Setting up
setup(
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