# Python Fakeports
Python fakeports is a clone of portspoof (see [http://drk1wi.github.io/portspoof/](http://drk1wi.github.io/portspoof/)) 
written in python with focus on finer control for Deception techniques.
Fakeports and allows you to configure specific TCP/UDP ports to simulate
services with matching signatures.

**Overall functionalities**

- Ability to parse and search through the _nmap-service-probes_ file.
- Automated setup of _iptable_ rules for current configuration.
- Support for both TCP and UDP connections
- Easy configuration with binary support using YAML files.
- Behavioural signature types as well as regular expressions and simple signatures

## Install
At this moment installation can be done using the following command:
```
cd python-fakeports
sudo python setup.py install
``` 

Once completed you can run `fakeportsctl` to control the software:
```
ubuntu@fakeportshost:~$ fakeportsctl 
Usage: fakeportsctl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  find      Find signature by program name
  info      Print detailed info about signature by id
  iptables  Add or remove the iptable rules from the...
  parse     Parse the nmap-service-probes file into a...
  run       Dry run the application

```

