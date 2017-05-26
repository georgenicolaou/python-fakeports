from setuptools import setup

setup(
    name='python-fakeports',
    version="0.1",
    packages=['python_fakeports'],
    url='',
    license='GPL',
    author='George Nicolaou',
    author_email='george@silensec.com',
    description='Python clone of portspoof',
    long_description="""TODO""",
    install_requires=[
        "Twisted==15.2.1",
        "PyYAML==3.11",
        "python-iptables==0.11.0",
        "netifaces==0.10.4"
    ],
    scripts=['bin/fakeportsctl', 'bin/fakeportsd', 'bin/fakeports.tac'],
    platforms='any'
)
