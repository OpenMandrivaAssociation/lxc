%define libname %mklibname %name 0

Name:           lxc
Version:        0.7.5
Release:        3
Summary:        Linux Resource Containers

Group:          System/Kernel and hardware
License:        LGPLv2+
URL:            http://lxc.sourceforge.net
Source0:        http://lxc.sourceforge.net/download/lxc/%{name}-%{version}.tar.gz
Patch0:		lxc-0.7.5-handle-automake-pkglib.patch

BuildRequires:  automake
BuildRequires:  docbook-utils
BuildRequires:  kernel-headers
BuildRequires:  libcap-devel
BuildRequires:  libtool
Buildrequires:	docbook-dtd30-sgml

%description
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

%package        -n %libname
Summary:        Runtime library files for %{name}
Group:          System/Libraries
Requires:       %{name} = %{version}

%description    -n %libname
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

This package contains libraries for running %{name} applications.

%package        devel
Summary:        Development files for %{name}
Group:          Development/C
Requires:       %{name} = %{version}
Requires:       pkgconfig

%description    devel
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .pkglib~

%build
./autogen.sh
%configure F77=no
# Fix binary-or-shlib-defines-rpath error
%{__sed} -i '/AM_LDFLAGS = -Wl,-E -Wl,-rpath -Wl,$(libdir)/d' src/lxc/Makefile.in
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/%{name}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/%{name}-*
%{_libexecdir}/%{name}
%{_mandir}/man*/%{name}*
%{_localstatedir}/lib/%{name}

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/liblxc.so.*

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/%{name}.pc
%{_includedir}/*
%{_libdir}/liblxc.so
