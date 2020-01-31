from setuptools import setup

long_description = 'TODO'
# with open("README.md", "r") as rfd:
#     long_description = rfd.read()

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
    install_requires=[
        "appdirs==1.4.3",
        "attrs==17.2.0",
        "Automat==0.6.0",
        "click==6.7",
        "constantly==15.1.0",
        "exrex==0.10.4",
        "incremental==17.5.0",
        "netifaces==0.10.4",
        "packaging==16.8",
        "pyparsing==2.2.0",
        "PyYAML==3.12",
        "six==1.10.0",
        "Twisted==19.7.0",
        "zope.interface==4.4.1",
        "python-iptables==0.11.0"
    ],
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
