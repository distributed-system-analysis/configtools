Name:        configtools
Version:     0.3.1
Release:     1
Summary:     The configtools module

License:     GPLv3+
URL:         https://pypi.python.org/pypi/%{name}
Source0:     https://pypi.python.org/packages/source/c/%{name}/%{name}-%{version}.tar.gz
Buildarch:   noarch

BuildRequires:	python3-devel

%description
The configtools python module and the getconf.py command-line script.

%prep
%setup -qn %{name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%files
/usr/bin/getconf.py
/usr/bin/gethosts.py
%{python_sitelib}/configtools
%{python_sitelib}/%{name}-%{version}-py*.egg-info

%doc
