%define libname %mklibname %name 0

Name:           lxc
Version:        0.7.4.2
Release:        %mkrel 1
Summary:        Linux Resource Containers

Group:          System/Kernel and hardware
License:        LGPLv2+
URL:            http://lxc.sourceforge.net
Source0:        http://lxc.sourceforge.net/download/lxc/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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

%package        doc
Summary:        Documentation for %{name}
Group:		Books/Other 
Requires:       %{name} = %{version}

%description    doc
This package contains documentation for %{name}.

%prep
%setup -q

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
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/%{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/%{name}-*
%{_libexecdir}/lxc
%{_mandir}/man*/%{name}*
%{_sharedstatedir}/%{name}

%files -n %libname
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/liblxc.so.*

%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_datadir}/pkgconfig/%{name}.pc
%{_includedir}/*
%{_libdir}/liblxc.so

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}

