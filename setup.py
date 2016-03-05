import setuptools
if __name__ == '__main__':
    setuptools.setup(
        test_suite='test_kron',
        name='kron',
        url='https://github.com/qtfkwk/kron',
        author='qtfkwk',
        author_email='qtfkwk+kron@gmail.com',
        version='1.0.1',
        install_requires=[
            'pytz',
            'tzlocal',
        ],
        py_modules=['kron'],
    )
