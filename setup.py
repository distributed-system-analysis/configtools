from distutils.core import setup

setup(name = 'configtools',
      version = '0.3.1',
      description = 'Simple set of tools to read and parse configuration files for use by shell scripts',
      author = 'Nick Dokos',
      author_email = 'ndokos@redhat.com',
      url = 'https://github.com/distributed-system/analysis/configtools',
      packages = ['configtools'],
      scripts = ['bin/getconf.py', 'bin/gethosts.py',],
     )
