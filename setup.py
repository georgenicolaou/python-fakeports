from setuptools import setup

long_description = 'TODO'
# with open("README.md", "r") as rfd:
#     long_description = rfd.read()
REQUIREMENTS = [r.strip() for r in open("requirements.txt").readlines()]

setup(
    name='python-fakeports',
    version="0.1",
    packages=['python_fakeports'],
    url='',
    license='GPL',
    author='George Nicolaou',
    author_email='george@silensec.com',
    description='Python clone of portspoof',
    long_description=long_description,
    install_requires=REQUIREMENTS,
    data_files=[
        ('/etc/fakeports/', ['fakeports.yml.sample']),
        ('/usr/local/bin/', ['bin/fakeports.tac'])
    ],
    scripts=['bin/fakeportsctl', 'bin/fakeportsd'],
    platforms='any',
    classifiers = [line.strip() for line in '''\
    Development Status :: 4 - Beta
    Intended Audience :: System Administrators
    Operating System :: POSIX :: Linux
    ''']
)
