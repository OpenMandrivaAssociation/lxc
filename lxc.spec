%define major 1
%define libname %mklibname lxc %{major}
%define develname %mklibname lxc -d
%define debugcflags	%nil
%define	debug_package	%nil

%define luaver 5.3
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}
# disable it untill https://github.com/lxc/lxc/issues/174
# not solved
%bcond_without	lua
%bcond_without	python

Name:		lxc
Version:	2.0.7
Release:	1
Summary:	Linux Containers
URL:		http://lxc.sourceforge.net
Source0:	http://linuxcontainers.org/downloads/%{name}-%{version}.tar.gz
Source1:	%{name}.sh
Source2:	dnsmasq-rule
Source3:	ifcfg-lxcbr0
Source4:	sysctl-rule
Source100:	lxc.rpmlintrc
Group:		System/Kernel and hardware
License:	LGPLv2
Epoch:		1
Patch0:         lxc-0.9.0.ROSA.network.patch
Patch1:         lxc-0.9.0.updates.patch
Patch2:		fix-node-device.patch
#Patch3:		fix-systemd-path.patch
Patch4:		lxc-1.0.5-lua-linkage.patch
BuildRequires:	docbook-utils
BuildRequires:  kernel-headers
BuildRequires:	cap-devel
BuildRequires:	pkgconfig(libsystemd)
Buildrequires:	docbook-dtd30-sgml
Buildrequires:	docbook2x
%if %{with lua}
Buildrequires:	lua-devel
%endif
%if %{with python}
Buildrequires:	python3-devel
%endif
# needed for lxc-busybox
Requires:       busybox
# needed for lxc-debian
Requires:       dpkg
# needed for lxc-debian, lxc-ubuntu:
Requires:       debootstrap rsync
# needed for lxc-sshd
Requires:       openssh-server
# bridge
Requires:	bridge-utils
# for lxcbr0
Requires:	iptables
Requires:	dnsmasq
# bash completion
Requires:	bash-completion

Conflicts:   lxc-doc < 0.7.5
Obsoletes:   lxc-doc < 0.7.5

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

%package -n	%{libname}
Summary:	Library for LXC
Group:		System/Libraries

%description -n %{libname}
Library for the Linux Kernel Containers.

%package -n	%{develname}
Summary:	Development files for LXC
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{develname}
Developement files for the Linux Kernel Containers.

%if %{with lua}
%package        -n lua-%{name}
Summary:        Lua binding for %{name}
Group:          System/Libraries
Requires:       lua-filesystem

%description    -n lua-%{name}
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The lua-%{name} package contains the Lua binding for %{name}.
%endif

%if %{with python}
%package        -n python-%{name}
Summary:        Python binding for %{name}
Group:          System/Libraries
%rename		python3-%{name}

%description    -n python-%{name}
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The python-%{name} package contains the Python3 binding for %{name}.
%endif

%prep
%setup -q
%apply_patches

# Clang spews a few more warnings than gcc...
sed -i -e 's,-Werror,,g' configure*

autoreconf -fi

%build
%ifarch %ix86
export CC=gcc
export CXX=g++
%endif

%configure \
		--disable-apparmor \
		--with-init-script=systemd \
		--with-distro=openmandriva \
%if %{with lua}
		--enable-lua \
%endif
%if %{with python}
		--enable-python \
%endif

# remove rpath ( rpmlint error )
# sed -i '/AM_LDFLAGS = -Wl,-E -Wl,-rpath -Wl,$(libdir)/d' src/lxc/Makefile.in
%make

%install
%makeinstall_std templatesdir=%{_datadir}/lxc/templates READMEdir=%{_libdir}/lxc/rootfs

mkdir -p %{buildroot}/var/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/dnsmasq.d/
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/
mkdir -p %{buildroot}%{_sysconfdir}/sysctl.d/
install %{SOURCE2} %{buildroot}%{_sysconfdir}/dnsmasq.d/lxc
install %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifcfg-lxcbr0
install %{SOURCE4} %{buildroot}%{_sysconfdir}/sysctl.d/99-lxc-oom.conf

# Fix up bogus pkgconfig files
sed -i -e 's,\${prefix}//,/,g' %{buildroot}%{_libdir}/pkgconfig/*

%files
%doc README MAINTAINERS NEWS ChangeLog AUTHORS CONTRIBUTING COPYING
%{_datadir}/%{name}/config/common.conf.d/README
%{_sysconfdir}/default/%{name}
%{_bindir}/lxc-*
%{_sbindir}/init.lxc
%dir %{_libexecdir}/lxc
%{_libexecdir}/lxc/lxc-*
%dir %{_libexecdir}/lxc/hooks
%{_libexecdir}/lxc/hooks/unmount-namespace
%dir %{_datadir}/lxc
%dir %{_datadir}/lxc/config
%dir %{_datadir}/lxc/hooks
%dir %{_datadir}/lxc/templates
%dir %{_datadir}/lxc/selinux
%dir %{_datadir}/lxc/config/common.conf.d
%{_datadir}/lxc/templates/*
%{_datadir}/lxc/hooks/*
%{_datadir}/lxc/selinux/lxc.*
%{_libdir}/lxc/rootfs/README
%{_mandir}/man*/%{name}*
%{_mandir}/ja/man*/*
%{_datadir}/%{name}/config/*.seccomp
%{_datadir}/%{name}/config/*.conf
%{_datadir}/lxc/lxc-patch.py
/var/lib/%{name}
%{_datadir}/%{name}/%{name}.functions
%{_sysconfdir}/dnsmasq.d/lxc
%{_sysconfdir}/sysconfig/network-scripts/ifcfg-lxcbr0
%{_unitdir}/lxc.service
%{_unitdir}/lxc-net.service
%{_sysconfdir}/sysctl.d/99-lxc-oom.conf
%{_sysconfdir}/lxc/default.conf
/lib/systemd/system/lxc@.service
%{_sysconfdir}/bash_completion.d/lxc
%lang(ko) %{_mandir}/ko/*/*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}
%{_libdir}/lib%{name}.so.%{major}.*

%files -n %{develname}
%doc COPYING
%{_includedir}/%{name}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%if %{with lua}
%files -n lua-%{name}
%{lualibdir}/%{name}
%{luapkgdir}/%{name}.lua
%endif

%if %{with python}
%files -n python-%{name}
%{python3_sitearch}/*
%endif
