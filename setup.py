# Name: kron
# Description: Uniform interface for dates and times in Python
# Version: 1.3.2
# File: setup.py
# Author: qtfkwk <qtfkwk+kron@gmail.com>
# Copyright: (C) 2016 by qtfkwk
# License: BSD 2-Clause License (https://opensource.org/licenses/BSD-2-Clause)

# External modules

import setuptools

# Main

if __name__ == '__main__':
    setuptools.setup(
        test_suite='test_kron',
        name='kron',
        url='https://github.com/qtfkwk/kron',
        author='qtfkwk',
        author_email='qtfkwk+kron@gmail.com',
        version='1.3.2',
        install_requires=[
            'ntplib',
            'pytz',
            'tzlocal',
        ],
        py_modules=['kron'],
        description='Uniform interface for dates and times',
        entry_points=dict(console_scripts=['kron = kron:main']),
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Topic :: Utilities',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )

