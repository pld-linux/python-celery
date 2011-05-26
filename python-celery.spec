# TODO
# - pldize initscript
# - fill descriptions and urls
%define 	module	celery
Summary:	Distributed Task Query
Name:		python-%{module}
Version:	2.2.6
Release:	0.3
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	0c8f5ec2535e2aaf692fd0227a5bb407
Source1:	celeryd.sysconfig
URL:		-
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
Requires:	python-amqplib
Requires:	python-anyjson
Requires:	python-dateutil < 2.0.0
Provides:	user(celery)
Requires(post,preun):	/sbin/chkconfig
Requires:	python-kombu
Requires:	python-modules
Requires:	rc-scripts
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
install -p contrib/generic-init.d/celeryd $RPM_BUILD_ROOT/etc/rc.d/init.d

## fixed path to celeryd configuration file.
sed -i 's/default/sysconfig/' $RPM_BUILD_ROOT/etc/rc.d/init.d/celeryd

## creating dummy celeryd config file
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/celeryd

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# XXX uid 300 not registered in PLD-doc/uid_gid.db.txt
%useradd -u 300 -g users -r -s /bin/false "celery user" celery

%post
/sbin/chkconfig --add celeryd
%service celeryd restart

%preun
if [ "$1" = "0" ]; then
	%service -q celeryd stop
	/sbin/chkconfig --del celeryd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove celery
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README* THANKS TODO
%attr(755,root,root) %{_bindir}/camqadm
%attr(755,root,root) %{_bindir}/celerybeat
%attr(755,root,root) %{_bindir}/celeryctl
%attr(755,root,root) %{_bindir}/celeryd
%attr(755,root,root) %{_bindir}/celeryd-multi
%attr(755,root,root) %{_bindir}/celeryev

%attr(754,root,root) /etc/rc.d/init.d/celeryd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/celeryd

%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/celery-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}

# XXX remove?
%{py_sitescriptdir}/funtests
