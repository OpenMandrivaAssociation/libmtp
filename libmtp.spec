%define major	9
%define	libname	%mklibname mtp %major
%define develname %mklibname -d mtp

Name:		libmtp
Summary:	Implementation of Microsoft's Media Transfer Protocol
Version:	1.1.5
Release:	1
Group:		System/Libraries
License:	LGPLv2+
URL:		http://libmtp.sourceforge.net/
Source0:	http://ignum.dl.sourceforge.net/project/libmtp/libmtp/%version/libmtp-%version.tar.gz
BuildRequires:	libusbx-devel doxygen

%track
prog %name = {
	url = http://sourceforge.net/projects/libmtp/files/libmtp/
	version = %version
	regex = "Download %name-(__VER__)\.tar\.gz"
}

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
Obsoletes:	%mklibname mtp 6
Requires:	%{name}-utils >= %{version}-%{release}

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
Provides: mtp-utils = %{version}-%{release}

%description utils
This package contains various tools provided by libmtp.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--enable-doxygen \
	--with-udev-rules=60-libmtp.rules
%make

%install
%makeinstall_std

#-- FEDORA COPY
mkdir -p %{buildroot}%{_datadir}/hal/fdi/information/10freedesktop
install -p -m 644 libmtp.fdi %{buildroot}%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi
#-- FEDORA COPY
# Replace links with relative links
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-delfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-getfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-newfolder
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-sendfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-sendtr
pushd $RPM_BUILD_ROOT%{_bindir}
ln -sf mtp-connect mtp-delfile
ln -sf mtp-connect mtp-getfile
ln -sf mtp-connect mtp-newfolder
ln -sf mtp-connect mtp-sendfile
ln -sf mtp-connect mtp-sendtr
popd

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}/html
mv -f %{buildroot}/%{_datadir}/doc/%{name}-%{version}/html/* %{buildroot}/%{_datadir}/doc/%{name}/html/

# don't ship .la
find %{buildroot} -name *.la | xargs rm -f

%files -n %{libname}
%doc AUTHORS COPYING README
%{_libdir}/libmtp.so.%{major}*

%files -n %{develname}
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*

%files doc
%doc %{_datadir}/doc/%{name}/html

%files utils
/lib/udev/rules.d/*.rules
%config(noreplace) %{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi
/lib/udev/mtp-probe
%{_bindir}/*
