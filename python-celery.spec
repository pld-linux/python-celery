%define 	module	celery
Summary:	Distributed Task Query
Summary(pl.UTF-8):	-
Name:		python-%{module}
Version:	2.2.6
Release:	0.1
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	0c8f5ec2535e2aaf692fd0227a5bb407
URL:		-
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README* THANKS TODO
%attr(755,root,root) %{_bindir}/camqadm
%attr(755,root,root) %{_bindir}/celerybeat
%attr(755,root,root) %{_bindir}/celeryctl
%attr(755,root,root) %{_bindir}/celeryd
%attr(755,root,root) %{_bindir}/celeryd-multi
%attr(755,root,root) %{_bindir}/celeryev
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/celery-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}

# XXX remove?
%{py_sitescriptdir}/funtests
