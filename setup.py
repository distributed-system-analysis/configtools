from distutils.core import setup

setup(name = 'configtools',
      version = '0.3',
      description = 'Simple tools for using config files',
      author = 'Nick Dokos',
      author_email = 'ndokos@redhat.com',
      url = 'http://foo',
      packages = ['configtools'],
      scripts = ['bin/getconf.py', 'bin/gethosts.py',],
     )
