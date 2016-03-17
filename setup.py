# Name: kron
# Description: Uniform interface for dates and times
# Version: 1.5.2
# File: setup.py
# Author: qtfkwk <qtfkwk+kron@gmail.com>
# Copyright: (C) 2016 by qtfkwk
# License: BSD 2-Clause License (https://opensource.org/licenses/BSD-2-Clause)

# External modules

import setuptools

# Internal modules

import kron

# Main

if __name__ == '__main__':
    setuptools.setup(
        test_suite='test_kron',
        name='kron',
        url='https://github.com/qtfkwk/kron',
        author='qtfkwk',
        author_email='qtfkwk+kron@gmail.com',
        version=kron.version,
        install_requires=[
            'ntplib',
            'pytz',
            'tzlocal',
        ],
        py_modules=['kron'],
        description='Uniform interface for dates and times',
        entry_points=dict(console_scripts=['kron = kron:_main']),
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Topic :: Utilities',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
        ],
    )

