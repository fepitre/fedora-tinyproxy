%define tinyproxy_confdir %{_sysconfdir}/tinyproxy
%define tinyproxy_datadir %{_datadir}/tinyproxy
%define tinyproxy_rundir  %{_localstatedir}/run/tinyproxy
%define tinyproxy_logdir  %{_localstatedir}/log/tinyproxy

Name:           tinyproxy
Version:        1.8.1
Release:        1%{?dist}
Summary:        A small, efficient HTTP/SSL proxy daemon

Group:          System Environment/Daemons
License:        GPLv2+
URL:            https://www.banu.com/tinyproxy/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        https://www.banu.com/pub/tinyproxy/1.8/%{name}-%{version}.tar.bz2
Source1:        %{name}.init
Source2:        %{name}.conf
Source3:        %{name}.logrotate

Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(preun):    initscripts
BuildRequires:      asciidoc

%description
tinyproxy is a small, efficient HTTP/SSL proxy daemon that is very useful in a
small network setting, where a larger proxy like Squid would either be too
resource intensive, or a security risk.  

%prep
%setup -q


%build
%configure --sysconfdir=%{tinyproxy_confdir} \
    --enable-reverse \
    --enable-transparent 

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{tinyproxy_confdir}/%{name}.conf
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0700 %{buildroot}%{_localstatedir}/run/%{name}
%{__install} -p -D -m 0700 %{buildroot}%{_localstatedir}/log/%{name}

%clean
rm -rf %{buildroot}


%post
/sbin/chkconfig --add %{name}
    

%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi  
    

%postun
if [ "$1" -ge "1" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi  
 


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS docs/*.txt
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man5/%{name}.conf.5.gz
%{_initrddir}/%{name}
%dir %{tinyproxy_datadir}
%dir %{tinyproxy_datadir}/*
%dir %{tinyproxy_confdir}
%dir %{tinyproxy_rundir}
%dir %{tinyproxy_logidr}
%config(noreplace) %{tinyproxy_confdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%changelog
* Tue Apr 06 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.8.1-1
- update to updstream 1.8.1

* Wed Feb 17 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.8.0-1
- update to upstream 1.8.0
- add logrotate configuration

* Sun Oct 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.5-1
- update to upstream 1.6.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.4-3
- add --enable-transparent-proxy option (#466808)

* Sun Aug 24 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.4-2
- update to upstream 1.6.4 final

* Sun Jun 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.4-1
- update to upstream candidate 1.6.4

* Wed Apr 16 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.3-2
- fix spec review issues
- fix initscript

* Sun Mar 09 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.3-1
- Initial rpm configuration
