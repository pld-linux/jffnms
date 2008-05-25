Summary:	JFFNMS - Network Management and Monitoring System
Name:		jffnms
Version:	0.8.3
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/jffnms/%{name}-%{version}.tar.gz
# Source0-md5:	6f030ee09302b67f639eaff713b78c65
URL:		http://www.jffnms.org/
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	crondaemon
Requires:	diffutils
Requires:	fping
Requires:	rrdtool > 1.0.33
Requires:	tmpwatch
Requires:	webapps
Requires:	webserver
Requires:	webserver(php) > 5.0.0
Requires:	webserver(php) >= 4.1.2
# snmp, ssl, gd, sockets, mysql, pgsql, pcre, posix, ob, pcntl, session, wddx
Provides:	group(jffnms)
Provides:	user(jffnms)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JFFNMS is a Network Management and Monitoring System designed to
monitor a IP SNMP / Syslog / Tacacs+ Network. It can be used to
monitor any standards compilant SNMP device, Server, Router, TCP port
or anything you want, if you write a custom poller, we also provide
some Cisco focused features.

Features:
- Written in PHP
- Status Map, gives you a quick look of your network
- Events Console, shows all kinds of events in the same time-ordered
  display
- Performance Graphs for everything, Interface Traffic, Errors, CPU
  Usage, etc.
- Database Backend (MySQL or PostgreSQL)
- Integrated Syslog Logging and Tacacs+ Authentication and Accounting
- and much more features

%prep
%setup -q
# undos the source
find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_var}/lib/%{name}/{logs,rrd,tftpd},%{_var}/spool/cron}
install docs/unix/crontab $RPM_BUILD_ROOT%{_var}/spool/cron/%{name}
rm -rf engine/windows
cp -rf {conf,engine,htdocs,lib}  $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post
%groupadd -g jffnms
%useradd -g jffnms -d %{_var}/lib/%{name} -s /bin/false -c 'JFFNMS User' -u jffnms
%addusertogroup http jffnms
echo jffnms >> /etc/cron.allow
%service -q crond restart

%postun
if [ "$1" = "0" ]; then
	%groupremove jffnms
	%userremove jffnms
	%service -q crond restart
fi

if [ -f /var/spool/cron/%{name} ]; then
	crontab -u %{name} -r
fi

%files
%defattr(644,root,root,755)
%doc BUGS INSTALL LICENSE UPGRADE Changelog TODO docs
%config(noreplace) %attr(640,jffnms,jffnms) %{_var}/spool/cron/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/htdocs
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/conf
%dir %{_datadir}/%{name}/engine
%{_datadir}/%{name}/engine/*.php
%attr(750,jffnms,jffnms) %{_datadir}/%{name}/engine/*.sh
%{_datadir}/%{name}/engine/pollers
%{_datadir}/%{name}/engine/graphs
%{_datadir}/%{name}/engine/discovery
%{_datadir}/%{name}/engine/satellite
%{_datadir}/%{name}/engine/consolidate
%{_datadir}/%{name}/engine/backends
%{_datadir}/%{name}/engine/tools
%{_datadir}/%{name}/engine/shared
%{_datadir}/%{name}/engine/actions
%{_datadir}/%{name}/engine/configs
%{_datadir}/%{name}/engine/handlers
%{_datadir}/%{name}/engine/trap_receivers
%{_datadir}/%{name}/engine/analyzers
%{_datadir}/%{name}/engine/fonts
%{_datadir}/%{name}/engine/ticket
%dir %attr(750,jffnms,jffnms) %{_var}/lib/%{name}
%dir %attr(750,jffnms,jffnms) %{_var}/lib/%{name}/logs
%dir %attr(750,jffnms,jffnms) %{_var}/lib/%{name}/rrd
%dir %attr(750,jffnms,jffnms) %{_var}/lib/%{name}/tftpd
