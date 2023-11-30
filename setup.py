"""
info:This module contains the implememntation of the SparkVerse Simulator
autor: Tucudean Adrian-Ionut
date: 25.11.2023
email: Tucudean.Adrian.Ionut@outlook.com
license: MIT
"""

import os
from setuptools import setup, find_packages
#from src.tucu.external_data import VERSION
here = os.path.abspath(os.path.dirname(__file__))
#README = open(os.path.join(here, 'README-pypi.rst')).read()



install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'requests'	
]


setup(name='taisim2',
    version='0.0.1',
    description="Simulation Library for Multi-Robot Systems",
    long_description="Simulation Library for Multi-Robot Systems",
    keywords='Simulator computer vision Advanced Driving',
    author='Tucudean Adrian-Ionut',
    author_email='Tucudean.Adrian.Ionut@outlook.com',
    url='https://github.com/Amporu/Taisim2',
    license='MIT',
    packages=find_packages('src','src/taisim2/data'),
    package_dir = {'': 'src'},include_package_data=True,
    package_data={'taisim':['data/*.png',"*.py"]},
    zip_safe=False,
    install_requires=['opencv-python','pygame','pyOpenGL'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
    'console_scripts': [
        'taisim2 = taisim2:main',
    ],
},
)