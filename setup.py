import setuptools
if __name__ == '__main__':
    setuptools.setup(
        test_suite='test_timestamp',
        name='timestamp',
        url='https://github.com/qtfkwk/timestamp',
        author='qtfkwk',
        author_email='qtfkwk+timestamp@gmail.com',
        version='1.0.0',
        install_requires=[
            'pytz',
            'tzlocal',
        ],
        py_modules=['timestamp'],
    )
