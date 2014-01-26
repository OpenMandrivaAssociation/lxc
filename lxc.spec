%define major 0
%define libname %mklibname lxc %{major}
%define develname %mklibname lxc -d
%define debugcflags	%nil
%define	debug_package	%nil

%define luaver 5.1
%define lualibdir %{_libdir}/lua/%{luaver}
%define luapkgdir %{_datadir}/lua/%{luaver}
%bcond_without	lua
%bcond_with	python3

Name:		lxc
Version:	0.9.0
Release:	23
Summary:	Linux Containers
URL:		http://lxc.sourceforge.net
Source0:	http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.sh
Source2:	dnsmasq-rule
Source3:	ifcfg-lxcbr0
Source4:	sysctl-rule
Group:		System/Kernel and hardware
License:	LGPLv2
Epoch:		1
Patch0:		lxc-0.9.0-fedora-template.patch
Patch1:		0001-Add-an-OpenMandriva-LX-template.patch
Patch2:         lxc-0.9.0.ROSA.network.patch
Patch3:         lxc-0.9.0.updates.patch
Patch4:		disable-werror-for-autoreconf.patch
BuildRequires:	docbook-utils
BuildRequires:  kernel-headers
BuildRequires:	cap-devel
Buildrequires:	docbook-dtd30-sgml
Buildrequires:	docbook2x
%if %{with lua}
Buildrequires:	lua-devel
%endif
%if %{with python3}
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

%if %{with python3}
%package        -n python3-%{name}
Summary:        Python binding for %{name}
Group:          System Environment/Libraries

%description    -n python3-%{name}
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The python3-%{name} package contains the Python3 binding for %{name}.
%endif

%prep
%setup -q
%apply_patches

%build
autoreconf -fiv
# Alexander Khryukin
# change --with-distro=mandriva to openmandriva
# after 1.0 release
# https://github.com/lxc/lxc/pull/66
%configure2_5x  F77=no \
		--disable-apparmor \
		--with-distro=mandriva \
%if %{with lua}
		--enable-lua \
%endif
%if %{with python3}
		--enable-python \
%endif

# remove rpath ( rpmlint error )
sed -i '/AM_LDFLAGS = -Wl,-E -Wl,-rpath -Wl,$(libdir)/d' src/lxc/Makefile.in
make

%install
%makeinstall_std templatesdir=%{_datadir}/lxc/templates READMEdir=%{_libexecdir}/lxc/rootfs

mkdir -p %{buildroot}/var/lib/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/bash_completion.d/
mkdir -p %{buildroot}%{_sysconfdir}/dnsmasq.d/
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/
mkdir -p %{buildroot}%{_sysconfdir}/sysctl.d/
install %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/bash_completion.d/lxc
install %{SOURCE2} %{buildroot}%{_sysconfdir}/dnsmasq.d/lxc
install %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifcfg-lxcbr0
install %{SOURCE4} %{buildroot}%{_sysconfdir}/sysctl.d/99-lxc-oom.conf

%files
%doc README MAINTAINERS NEWS TODO ChangeLog AUTHORS CONTRIBUTING COPYING
%{_bindir}/lxc-*
%{_libexecdir}/lxc/lxc-init
%{_datadir}/lxc/templates/*
%{_datadir}/lxc/hooks/*
%{_libexecdir}/lxc/rootfs/README
%{_mandir}/man*/%{name}*
/var/lib/%{name}
%{_datadir}/%{name}/%{name}.functions
%{_sysconfdir}/%{name}/bash_completion.d/lxc
%{_sysconfdir}/dnsmasq.d/lxc
%{_sysconfdir}/sysconfig/network-scripts/ifcfg-lxcbr0
%{_sysconfdir}/sysctl.d/99-lxc-oom.conf
/etc/lxc/default.conf

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

%if %{with python3}
%files -n python3-%{name}
%{python3_sitearch}/*
%endif
