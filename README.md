# configtools
Simple set of tools to read and parse configuration files for use by shell scripts

## Installation
Simple setuptools based Python project, see `setup.py`, can be installed from
source using `python setup.py install`.

### PyPI
Available via PyPI, see http://pypi.python.org/configtools

```
pip install configtools
```

### Fedora COPR Available via Fedora's COPR, see
http://copr.fedoraproject.org/coprs/portante/configtools/

To make your own COPR build, first make sure the `configtools.spec` file points
the proper version from PyPI.  Then pull the source tar ball locally from
PyPI, .e.g. `wget
https://pypi.python.org/packages/source/c/configtools/configtools-0.3.tar.gz#md5=ca44cd06d26807805e433731dc5c085e
-O /tmp/configtools-0.3.tar.gz`, then do the following:

1. `mkdir -p $HOME/rpmbuild/SPECS $HOME/rpmbuild/SOURCES`
2. `cp ./configtools.spec $HOME/rpmbuild/SPECS/`
3. `cp /tmp/configtools-0.3.tar.gz $HOME/rpmbuild/SOURCES/`
4. `cd $HOME/rpmbuild/SPECS`
5. `rpmbuild -bs configtools.spec`
6. Upload the resulting SRPM in
   `$HOME/rpmbuild/SRPMS/configtools-0.3.srpm` to your COPR project for
   configtools

## History
Developed to help the pbench sister project handle configuration files from
the various shell scripts in that project. See
https://github.com/distributed-system-analysis/pbench.
