
# TODO:
#	- consider init script / systemd job (uid/gid celery 274 used to be used)
#	  NOTE: this must not be included and enabled by default in the default
#	  package! Real-life deployments will mostly be application-specific.

# Conditional build:
%bcond_with	doc		# Sphinx documentation (too much dependencies to be worth the trouble)
%bcond_with	tests		# run tests (broken)
%bcond_without	python2 	# CPython 2.x module
%bcond_with	python3 	# CPython 3.x module (built from python3-celery.spec)
%bcond_with	python3_default	# Use Python 3.x for celery executables

%if %{without python3}
%undefine	python3_default
%endif

%define 	module	celery
Summary:	Celery - Distributed Task Query
Summary(pl.UTF-8):	Celery - rozproszona kolejka zadań
Name:		python-%{module}
# keep 4.x here for python2 support
Version:	4.4.7
Release:	1
License:	BSD-like
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/celery/
Source0:	https://files.pythonhosted.org/packages/source/c/celery/%{module}-%{version}.tar.gz
# Source0-md5:	62906067bd50c4e7e97f0b27f44f6bac
Patch0:		pytz_dependency.patch
URL:		http://celeryproject.org/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-billiard >= 3.6.3.0
BuildRequires:	python-billiard < 4
BuildRequires:	python-boto3 >= 1.9.178
BuildRequires:	python-case >= 1.3.1
BuildRequires:	python-dateutil >= 2.1
BuildRequires:	python-kombu >= 4.6.10
BuildRequires:	python-kombu < 4.7
BuildRequires:	python-mock >= 1.0.1
BuildRequires:	python-moto >= 1.3.7
BuildRequires:	python-pytest >= 4.6
BuildRequires:	python-pytz
BuildRequires:	python-vine >= 1.3.0
BuildRequires:	python-vine < 5
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 2
BuildRequires:	python3-billiard >= 3.6.3.0
BuildRequires:	python3-billiard < 4
BuildRequires:	python3-boto3 >= 1.9.178
BuildRequires:	python3-case >= 1.3.1
BuildRequires:	python3-dateutil >= 2.1
BuildRequires:	python3-kombu >= 4.6.10
BuildRequires:	python3-kombu < 4.7
BuildRequires:	python3-mock >= 1.0.1
BuildRequires:	python3-moto >= 1.3.7
BuildRequires:	python3-pytest >= 4.6
BuildRequires:	python3-pytz
BuildRequires:	python3-sphinx_testing
BuildRequires:	python3-vine >= 1.3.0
BuildRequires:	python3-vine < 5
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-billiard
BuildRequires:	python3-django
BuildRequires:	python3-kombu
BuildRequires:	python3-pytz
BuildRequires:	python3-sphinx_celery >= 2.0.0
BuildRequires:	python3-sphinxcontrib-issuetracker
BuildRequires:	python3-vine >= 1.3.0
BuildRequires:	python3-vine < 5
BuildRequires:	sphinx-pdg-3 >= 2
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

%description -l pl.UTF-8
Celery to asynchroniczna kolejka zadań oparta na rozproszonym
przekazywaniu komunikatów. Skupia się na działaniu w czasie
rzeczywistym, ale obsługuje też szeregowanie.

%package -n python3-%{module}
Summary:	Celery - Distributed Task Query
Summary(pl.UTF-8):	Celery - rozproszona kolejka zadań
Group:		Development/Languages/Python

%description -n python3-%{module}
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

%description -n python3-%{module} -l pl.UTF-8
Celery to asynchroniczna kolejka zadań oparta na rozproszonym
przekazywaniu komunikatów. Skupia się na działaniu w czasie
rzeczywistym, ale obsługuje też szeregowanie.

%package -n celery
Summary:	Celery - Distributed Task Query
Summary(pl.UTF-8):	Celery - rozproszona kolejka zadań
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

%description -n celery -l pl.UTF-8
Celery to asynchroniczna kolejka zadań oparta na rozproszonym
przekazywaniu komunikatów. Skupia się na działaniu w czasie
rzeczywistym, ale obsługuje też szeregowanie.

%package apidocs
Summary:	API documentation for Celery
Summary(pl.UTF-8):	Dokumentacja API Celery
Group:		Documentation
Obsoletes:	python3-celery-apidocs < 4.4.7

%description apidocs
API documentation for Celery.

%description apidocs -l pl.UTF-8
Dokumentacja API Celery.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=case.pytest \
%{__python} -m pytest t/unit -k 'not test_sphinx' -vv
# celery.contrib.sphinx expects Sphinx 2+
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=case.pytest \
%{__python3} -m pytest t/unit
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{celery,celery-2}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{celery,celery-3}

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'

%if %{with python3_default}
ln -sf celery-3 $RPM_BUILD_ROOT%{_bindir}/celery
%endif
%endif

%if %{without python3_default}
ln -sf celery-2 $RPM_BUILD_ROOT%{_bindir}/celery
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt Changelog.rst LICENSE README.rst TODO extra/{generic-init.d,supervisord,systemd}
%attr(755,root,root) %{_bindir}/celery-2
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/celery-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt Changelog.rst LICENSE README.rst TODO extra/{generic-init.d,supervisord,systemd}
%attr(755,root,root) %{_bindir}/celery-3
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/celery-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/.build2/html/*
%endif

%files -n celery
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/celery
