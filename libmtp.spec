%define major 9
%define libname %mklibname mtp %{major}
%define devname %mklibname -d mtp

%define _disable_rebuild_configure 1

Name:		libmtp
Summary:	Implementation of Microsoft's Media Transfer Protocol
Version:	1.1.16
Release:	3
Group:		System/Libraries
License:	LGPLv2+
Url:		http://libmtp.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/libmtp/libmtp/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	doxygen
BuildRequires:	pkgconfig(libusb-1.0)

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

%package utils
Summary:	Tools provided by libmtp
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	mtp-utils = %{version}-%{release}

%description utils
This package contains various tools provided by libmtp.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Suggests:	%{name}-utils >= %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package doc
Summary:	Libmtp documentation
Group:		Books/Computer books

%description doc
This package contains documentation of libmtp.

%prep
%setup -q
%autopatch -p1

%build
%configure \
	--disable-static \
	--enable-doxygen \
	--with-udev=/lib/udev \
	--with-udev-rules=60-libmtp.rules
%make

%install
%makeinstall_std

#-- FEDORA COPY
mkdir -p %{buildroot}%{_datadir}/hal/fdi/information/10freedesktop
install -p -m 644 libmtp.fdi %{buildroot}%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi
#-- FEDORA COPY
# Replace links with relative links
rm -f %{buildroot}%{_bindir}/mtp-delfile
rm -f %{buildroot}%{_bindir}/mtp-getfile
rm -f %{buildroot}%{_bindir}/mtp-newfolder
rm -f %{buildroot}%{_bindir}/mtp-sendfile
rm -f %{buildroot}%{_bindir}/mtp-sendtr
pushd %{buildroot}%{_bindir}
ln -sf mtp-connect mtp-delfile
ln -sf mtp-connect mtp-getfile
ln -sf mtp-connect mtp-newfolder
ln -sf mtp-connect mtp-sendfile
ln -sf mtp-connect mtp-sendtr
popd

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}/html
mv -f %{buildroot}/%{_datadir}/doc/%{name}-%{version}/html/* %{buildroot}/%{_datadir}/doc/%{name}/html/

%files utils
/lib/udev/rules.d/*.rules
/lib/udev/hwdb.d/*.hwdb
%config(noreplace) %{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi
/lib/udev/mtp-probe
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libmtp.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*

%files doc
%doc %{_datadir}/doc/%{name}/html
