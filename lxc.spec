%global _disable_rebuild_configure 0
# The python module doesn't link to libpython
%global _disable_ld_no_undefined 1

%define major 1
%define libname %mklibname lxc
%define oldlibname %mklibname lxc 1
%define develname %mklibname lxc -d
%define debugcflags %nil
%define debug_package %nil

Name:		lxc
Version:	6.0.3
Release:	1
Summary:	Linux Containers
Group:		System/Kernel and hardware
License:	LGPLv2
URL:		https://lxc.sourceforge.net
Source0:	http://linuxcontainers.org/downloads/lxc/%{name}-%{version}.tar.gz
Source4:	%{name}.sh
Source5:	dnsmasq-rule
Source6:	ifcfg-lxcbr0
Source7:	sysctl-rule
Source100:	lxc.rpmlintrc
BuildRequires:	docbook-utils
BuildRequires:	kernel-release-headers
BuildRequires:	cap-devel
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(dbus-1)
Buildrequires:	docbook-dtd30-sgml
Buildrequires:	docbook2x
BuildRequires:	pkgconfig(bash-completion)
%if %{with lua}
Buildrequires:	lua-devel
%endif
%if %{with python}
Buildrequires:	pkgconfig(python3)
Buildrequires:	python-setuptools
%endif
# needed for lxc-busybox
#Requires:	busybox
# needed for lxc-debian
#Requires:	dpkg
# needed for lxc-debian, lxc-ubuntu:
#Requires:	debootstrap
Requires:	rsync
# needed for lxc-sshd
Requires:	openssh-server
# bridge
Requires:	bridge-utils
# for lxcbr0
Requires:	iptables
Requires:	dnsmasq

Conflicts:	lxc-doc < 0.7.5
Obsoletes:	lxc-doc < 0.7.5

BuildSystem:	meson

%description
The package "%{name}" provides the command lines to create and manage
containers.  It contains a full featured container with the isolation
/ virtualization of the pids, the ipc, the utsname, the mount points,
/proc, /sys, the network and it takes into account the control groups.
It is very light, flexible, and provides a set of tools around the
container like the monitoring with asynchronous events notification,
or the freeze of the container. This package is useful to create
Virtual Private Server, or to run isolated applications like bash or
sshd.

%package -n %{libname}
Summary:	Library for LXC
Group:		System/Libraries
# Renamed 2025-02-26 before 6.0
%rename %{oldlibname}

%description -n %{libname}
Library for the Linux Kernel Containers.

%package -n %{develname}
Summary:	Development files for LXC
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{develname}
Developement files for the Linux Kernel Containers.

%if %{with lua}
%package -n lua-%{name}
Summary:	Lua binding for %{name}
Group:		System/Libraries
Requires:	lua-filesystem

%description -n lua-%{name}
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The lua-%{name} package contains the Lua binding for %{name}.
%endif

%if %{with python}
%package  -n python-%{name}
Summary:	Python binding for %{name}
Group:		System/Libraries
%rename		python3-%{name}

%description -n python-%{name}
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The python-%{name} package contains the Python3 binding for %{name}.
%endif

%files
%dir %{_sysconfdir}/lxc
%config %{_sysconfdir}/lxc/default.conf
%config %{_sysconfdir}/sysconfig/lxc
%{_bindir}/init.lxc
%{_bindir}/lxc-*
%{_unitdir}/lxc-monitord.service
%{_unitdir}/lxc-net.service
%{_unitdir}/lxc.service
%{_unitdir}/lxc@.service
%{_libexecdir}/lxc
%{_libdir}/lxc
%{_datadir}/lxc
%{_datadir}/bash-completion/completions/*
%doc %{_docdir}/lxc
%lang(ja) %{_mandir}/ja/*/*.*
%lang(ko) %{_mandir}/ko/*/*.*
%{_mandir}/man?/*.*

%files -n %{develname}
%{_includedir}/lxc
%{_libdir}/liblxc.so
%{_libdir}/liblxc.a
%{_libdir}/pkgconfig/lxc.pc

%files -n %{libname}
%{_libdir}/liblxc.so.1*
