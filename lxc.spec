%global _disable_rebuild_configure 0
# The python module doesn't link to libpython
%global _disable_ld_no_undefined 1

%define major 1
%define libname %mklibname lxc %{major}
%define develname %mklibname lxc -d
%define debugcflags %nil
%define debug_package %nil

%define luaver 5.4
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}
# disable it untill https://github.com/lxc/lxc/issues/174
# not solved
%bcond_without lua
%bcond_without python

Name:		lxc
Version:	4.0.6
Release:	2
Summary:	Linux Containers
Group:		System/Kernel and hardware
License:	LGPLv2
Epoch:		1
URL:		http://lxc.sourceforge.net
Source0:	http://linuxcontainers.org/downloads/%{name}-%{version}.tar.gz
Source1:	http://linuxcontainers.org/downloads/%{name}-templates-3.0.4.tar.gz
Source2:	http://linuxcontainers.org/downloads/lua-%{name}-3.0.2.tar.gz
Source3:	http://linuxcontainers.org/downloads/python3-%{name}-3.0.4.tar.gz
Source4:	%{name}.sh
Source5:	dnsmasq-rule
Source6:	ifcfg-lxcbr0
Source7:	sysctl-rule
Source100:	lxc.rpmlintrc
Patch0:		lxc-templates-openmandriva.patch
Patch3:		lxc-1.0.5-lua-linkage.patch
Patch4:		lxc-3.1.0-python-linkage.patch
BuildRequires:	docbook-utils
BuildRequires:	kernel-release-headers
BuildRequires:	cap-devel
BuildRequires:	pkgconfig(libsystemd)
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

%prep
%setup -a 1 -a 2 -a 3
%autopatch -p1

# Clang spews a few more warnings than gcc...
sed -i -e 's,-Werror,,g' configure*

[ -e autogen.sh ] && ./autogen.sh || autoreconf -fi
cd lxc-templates-*
[ -e autogen.sh ] && ./autogen.sh || autoreconf -fi
cd ../lua-lxc-*
[ -e autogen.sh ] && ./autogen.sh || autoreconf -fi

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

%make_build

cd lxc-templates-*
%configure
%make_build

cd ../lua-lxc-*
%configure
%make_build

cd ..
export PKG_CONFIG_PATH=`pwd`
cd python3-lxc-*
python setup.py build

%install
%make_install templatesdir=%{_datadir}/lxc/templates READMEdir=%{_libdir}/lxc/rootfs
cd lxc-templates-*
%make_install templatesdir=%{_datadir}/lxc/templates READMEdir=%{_libdir}/lxc/rootfs
cd ../lua-lxc-*
%make_install templatesdir=%{_datadir}/lxc/templates READMEdir=%{_libdir}/lxc/rootfs
cd ../python3-lxc-*
python setup.py install --skip-build --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
cd ..

mkdir -p %{buildroot}/var/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/dnsmasq.d/
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/
mkdir -p %{buildroot}%{_sysconfdir}/sysctl.d/
install %{SOURCE4} %{buildroot}%{_sysconfdir}/dnsmasq.d/lxc
install %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifcfg-lxcbr0
install %{SOURCE6} %{buildroot}%{_sysconfdir}/sysctl.d/99-lxc-oom.conf

# Fix up bogus pkgconfig files
sed -i -e 's,\${prefix}//,/,g' %{buildroot}%{_libdir}/pkgconfig/*

%files
%doc %{_docdir}/%{name}
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
%doc %{_mandir}/man*/%{name}*
%doc %{_mandir}/ja/man*/*
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
%{_unitdir}/lxc@.service
%{_datadir}/bash-completion/completions/lxc
%lang(ko) %{_mandir}/ko/*/*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}
%{_libdir}/lib%{name}.so.%{major}.*

%files -n %{develname}
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
