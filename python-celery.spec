#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

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
# remove BR: python-devel for 'noarch' packages.
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
#Requires:		python-libs
Requires:		python-modules
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%prep
%setup -q -n %{module}-%{version}

# fix #!/usr/bin/env python -> #!/usr/bin/python:
# %{__sed} -i -e '1s,^#!.*python,#!%{__python},' %{name}.py

%build
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%{py_sitedir}/*.py[co]
%attr(755,root,root) %{py_sitedir}/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/TEMPLATE-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
