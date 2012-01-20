%define major	9
%define	libname	%mklibname mtp %major
%define develname %mklibname -d mtp

Name:		libmtp
Summary:	Implementation of Microsoft's Media Transfer Protocol
Version:	1.1.2
Release:	2
Group:		System/Libraries
License:	LGPLv2+
URL:		http://libmtp.sourceforge.net/
Source0:	http://nchc.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Patch0:		01-devices_small_fixes.patch
BuildRequires:	libusb-devel
BuildRequires:	doxygen
#gw for aclocal:
BuildRequires:	gettext-devel
Requires:	udev
Obsoletes:	%{name}-doc < %{version}

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

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Obsoletes:	%mklibname mtp 5
Obsoletes:	%mklibname mtp 0
Obsoletes:	%mklibname mtp 6
Obsoletes:	%mklibname mtp 8
Requires:	%{name}-utils >= %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d mtp 5
Obsoletes:	%mklibname -d mtp 0

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package utils
Summary:	Tools provided by libmtp
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	mtp-utils = %{version}-%{release}

%description utils
This package contains various tools provided by libmtp.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--disable-rpath

%make

%install
%makeinstall_std
find %{buildroot} -type f -name '*.la' -exec rm -f {} \;


%files -n %{libname}
%doc AUTHORS COPYING README
%{_libdir}/libmtp.so.%{major}*

%files -n %{develname}
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*

%files utils
/lib/udev/rules.d/*.rules
%{_bindir}/*
/lib/udev/mtp-probe
