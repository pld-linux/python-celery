
# TODO:
#	- consider init script / systemd job (uid/gid celery 274 used to be used)
#	  NOTE: this must not be included and enabled by default in the default
#	  package! Real-life deployments will mostly be application-specific.

# Conditional build:
%bcond_with	doc		# do build doc (too much dependencies to be worth the trouble)
%bcond_with	tests		# run tests (broken)
%bcond_without	python2 	# CPython 2.x module
%bcond_with	python3 	# CPython 3.x module
%bcond_with	python3_default	# Use Python 3.x for celery executables

%if %{without python3}
%undefine	python3_default
%endif

%define 	module	celery
Summary:	Celery - Distributed Task Query
Name:		python-%{module}
# keep python 2 version 4.x here; python3 in python3-celery.spec
Version:	4.4.0
Release:	3
License:	BSD-like
Group:		Development/Languages/Python
# Source0:	https://files.pythonhosted.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
Source0:	https://pypi.debian.net/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	9c5d17291bf204662ecc972eec26789e
Source1:	amqp-objects.inv
Source2:	cyme-objects.inv
Source3:	djcelery-objects.inv
Source4:	kombu-objects.inv
Source5:	python-objects.inv
Patch0:		pytz_dependency.patch
URL:		http://celeryproject.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
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
BuildRequires:	sphinx-pdg-2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose
%endif
%if %{with doc}
BuildRequires:	python3-billiard
BuildRequires:	python3-django
BuildRequires:	python3-kombu
BuildRequires:	python3-pytz
BuildRequires:	python3-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg-3
%endif
%endif
Requires:	python-billiard >= 3.5.0.2
Requires:	python-kombu >= 4.2.0
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
Requires:	python3-billiard >= 3.5.0.2
Requires:	python3-billiard < 4.0
Requires:	python3-kombu >= 4.2.0
Requires:	python3-kombu < 5.0
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

%package -n python3-%{module}-apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description -n python3-%{module}-apidocs
API documentation for %{module}.

%description -n python3-%{module}-apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%patch0 -p1

cp -a %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} docs

%build
%if %{with python2}
%py_build %{?with_tests:test}

%if %{with doc}
cd docs
PYTHONPATH=../build-2/lib %{__make} -j1 html SPHINXBUILD=sphinx-build-2
rm -rf .build/html/_sources
mv .build .build2
cd ..
%endif
%endif
%if %{with python3}
%py3_build %{?with_tests:test}

%if %{with doc} && 0
cd docs
PYTHONPATH=../build-3/lib %{__make} -j1 html SPHINXBUILD=sphinx-build-3
rm -rf .build/html/_sources
mv .build .build3
cd ..
%endif
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

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt LICENSE README.rst TODO extra
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/celery-*.egg-info
%{_examplesdir}/%{name}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/.build2/html/*
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt LICENSE README.rst TODO extra
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/celery-*.egg-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc} && 0
%files -n python3-%{module}-apidocs
%defattr(644,root,root,755)
%doc docs/.build3/html/*
%endif
%endif

%files -n celery
%attr(755,root,root) %{_bindir}/*
