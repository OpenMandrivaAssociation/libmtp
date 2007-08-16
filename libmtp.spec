%define	name	libmtp
%define	version	0.2.1
%define release %mkrel 1
%define major	6
%define	libname	%mklibname mtp %major
%define develname %mklibname -d mtp

Name:		%{name}
Summary:	Implementation of Microsoft's Media Transfer Protocol
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	LGPL
URL:		http://libmtp.sourceforge.net/
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	pkgconfig libusb-devel doxygen

%description
libmtp is an implementation of Microsoft's Media Transfer Protocol (MTP)
in the form of a library suitable primarily for POSIX compliant 
operating systems. We implement MTP Basic, the stuff proposed for 
standardization. MTP Enhanced is for Windows only, if we implement 
it, well that depends...

It was initially based on (forked from) the great libptp2 library 
by Mariusz Woloszyn but has since been moved over to follow Marcus 
Meissners and Hubert Figuere's libgphoto2 fork of libptp2 (or is libptp2
 a fork of libgphoto?). The core implementation is identical to 
libgphoto2, there is just a different API adapted to portable media 
players.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Obsoletes:	%mklibname mtp 5
Obsoletes:	%mklibname mtp 0

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d mtp 5
Obsoletes:	%mklibname -d mtp 0

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package doc
Summary: Libmtp documentation
Group: Books/Computer books

%description doc
This package contains documentation of libmtp.

%package utils
Summary: Tools provided by libmtp
Group: System/Libraries
Requires: %{libname} = %{version}-%{release}

%description utils
This package contains various tools provided by libmtp.

%prep
%setup -q

%build
%configure2_5x --enable-hotplugging --disable-static --program-prefix=mtp-
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}/html
mv -f %{buildroot}/%{_datadir}/doc/%{name}-%{version}/html/* %{buildroot}/%{_datadir}/doc/%{name}/html/

%clean 
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING README
%{_libdir}/libmtp.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/%{name}.la
%{_libdir}/pkgconfig/*

%files doc
%defattr(-,root,root)
%doc %{_datadir}/doc/%{name}/html

%files utils
%defattr(-,root,root)
%{_bindir}/*
