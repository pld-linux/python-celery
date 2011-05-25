%define 	module	celery
Summary:	Distributed Task Query
Summary(pl.UTF-8):	-
Name:		python-%{module}
Version:	2.2.6
Release:	0.3
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	0c8f5ec2535e2aaf692fd0227a5bb407
URL:		-
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
Requires:	python-kombu
Requires:	python-anyjson
Requires:	python-dateutil < 2.0.0
Requires:	python-amqplib
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

install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
cp -a contrib/generic-init.d/celeryd $RPM_BUILD_ROOT/etc/rc.d/init.d/

## fixed path to celeryd configuration file.
sed -i 's/default/sysconfig/' $RPM_BUILD_ROOT/etc/rc.d/init.d/celeryd

## creating dummy celeryd config file
cat > $RPM_BUILD_ROOT/etc/sysconfig/celeryd << EOF
#   # List of nodes to start
#   CELERYD_NODES="worker1 worker2 worker3"k
#   # ... can also be a number of workers
#   CELERYD_NODES=3
#
#   # Where to chdir at start.
#   CELERYD_CHDIR="/opt/Myproject/"
#
#   # Extra arguments to celeryd
#   CELERYD_OPTS="--time-limit=300"
#
#   # Name of the celery config module.#
#   CELERY_CONFIG_MODULE="celeryconfig"
EOF

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 300 -g users -r -s /bin/fafse "celery user" celery

%preun
/etc/rc.d/init.d/%{module}d stop

%post
echo "Use: \"/etc/rc.d/init.d/%{module}d start\" to start celry."

%postun
%userremove celery

%files
%defattr(644,root,root,755)
%doc AUTHORS README* THANKS TODO
%attr(755,root,root) %{_bindir}/camqadm
%attr(755,root,root) %{_bindir}/celerybeat
%attr(755,root,root) %{_bindir}/celeryctl
%attr(755,root,root) %{_bindir}/celeryd
%attr(755,root,root) %{_bindir}/celeryd-multi
%attr(755,root,root) %{_bindir}/celeryev

%attr(744,root,root) /etc/rc.d/init.d/*
%attr(644,root,root) /etc/sysconfig/*

%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/celery-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}

# XXX remove?
%{py_sitescriptdir}/funtests
