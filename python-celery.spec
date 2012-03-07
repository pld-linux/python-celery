%define 	module	celery
Summary:	Distributed Task Query
Name:		python-%{module}
Version:	2.5.1
Release:	0.3
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	c0912f29b69929219b353c748e0bf936
Source1:	celeryd.sysconfig
Source2:	celeryd.init
URL:		http://celeryproject.org/
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
Requires:	python-amqplib
Requires:	python-anyjson >= 0.3.1
Requires:	python-dateutil >= 1.5
Requires:	python-dateutil < 2.0.0
Requires(post,preun):	/sbin/chkconfig
Requires:	python-kombu >= 2.1.1
Requires:	python-modules
Requires:	rc-scripts
Provides:	user(celery)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

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

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/celeryd
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/celeryd

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 274 celery
%useradd -u 274 -g celery -r -s /bin/false "Celery Daemon" celery

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
	%groupremove celery
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS Changelog FAQ README THANKS TODO
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
