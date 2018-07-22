from setuptools import setup, find_packages

setup(
    name='lw301-server',
    version='0.0.1',
    install_requires=['tornado>=5.1, <6.0'],
    tests_require=['nose', 'pycodestyle'],
    test_suite='nose.collector',
    scripts=['lw301_server'],
    packages=find_packages(exclude=['lw301_server_tests']),
    description='Emulate servers for Oregon Scientific LW301',
    author='Nikita Kovalev',
    author_email='nikita@maizy.ru',
    license='Apache 2.0',
    url='https://github.com/maizy/lw301_server',
)
