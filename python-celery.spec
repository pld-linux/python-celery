
# TODO:
#	- consider init script / systemd job (uid/gid celery 274 used to be used)
#	  NOTE: this must not be included and enabled by default in the default
#	  package! Real-life deployments will mostly be application-specific.

# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests		# run tests (broken)
%bcond_without	python2 	# CPython 2.x module
%bcond_without	python3 	# CPython 3.x module
%bcond_without	python3_default	# Use Python 3.x for celery executables

%if %{without python3}
%undefine	python3_default
%endif

%define 	module	celery
Summary:	Celery - Distributed Task Query
Name:		python-%{module}
Version:	3.1.19
Release:	1
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	fba8c4b269814dc6dbc36abb0e66c384
Source1:	amqp-objects.inv
Source2:	cyme-objects.inv
Source3:	djcelery-objects.inv
Source4:	kombu-objects.inv
Source5:	python-objects.inv
Patch0:		pytz_dependency.patch
Patch1:		unittest2.patch
Patch2:		intersphinx.patch
URL:		http://celeryproject.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock >= 1.0.1
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-nose
%endif
%if %{with doc}
BuildRequires:	python-billiard
BuildRequires:	python-django
BuildRequires:	python-kombu
BuildRequires:	python-pytz
BuildRequires:	python-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg
%endif
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose
%endif
%endif
Requires:	python-billiard >= 3.3.0.21
Requires:	python-kombu >= 3.0.29
Requires:	python-pytz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

%package -n python3-%{module}
Summary:	Celery - Distributed Task Query
Group:		Development/Languages/Python
Requires:	python3-billiard >= 3.3.0.21
Requires:	python3-billiard < 3.4
Requires:	python3-kombu >= 3.0.29
Requires:	python3-kombu < 3.1
Requires:	python3-pytz

%description -n python3-%{module}
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

%package -n celery
Summary:	Celery - Distributed Task Query
Group:		Development/Languages/Python
%if %{with python3_default}
Requires:	python3-%{module} = %{version}
%else
Requires:	python-%{module} = %{version}
%endif

%description -n celery
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

cp -a %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} docs

%build
%if %{with python2}
%py_build %{?with_tests:test}

%if %{with doc}
cd docs
PYTHONPATH=../build-2/lib %{__make} -j1 html
rm -rf .build/html/_sources
cd ..
%endif
%endif
%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

install_python2() {
	%py_install

	%py_postclean
}
install_python3() {
	%py3_install
}

# install the right executables last
%if %{with python3} && %{without python3_default}
install_python3
%endif
%if %{with python2}
install_python2
%endif
%if %{with python3} && %{with python3_default}
install_python3
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt Changelog LICENSE README.rst TODO extra
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/celery-*.egg-info
%{_examplesdir}/%{name}-%{version}

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt Changelog LICENSE README.rst TODO extra
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/celery-*.egg-info
%{_examplesdir}/python3-%{module}-%{version}

%files -n celery
%attr(755,root,root) %{_bindir}/*

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/.build/html/*
%endif
