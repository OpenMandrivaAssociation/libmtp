%define	name	libmtp
%define	version	0.3.6
%define release %mkrel 1
%define major	8
%define	libname	%mklibname mtp %major
%define develname %mklibname -d mtp

Name:		%{name}
Summary:	Implementation of Microsoft's Media Transfer Protocol
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	LGPLv2+
URL:		http://libmtp.sourceforge.net/
Source0:	http://nchc.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	libmtp.perms
Patch0:		libmtp-0.3.5-fix-str-fmt.patch
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
%patch0 -p0

%build
%configure2_5x --disable-static --program-prefix=mtp-
%make
#-- FEDORA COPY
# Remove permissions from symlink in udev script, we use
# PAM to fix the permissions instead.
examples/hotplug -a"SYMLINK+=\"libmtp-%k\"" > libmtp.rules
#-- FEDORA COPY

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#-- FEDORA COPY
# Install udev rules file.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install -p -m 644 libmtp.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/60-libmtp.rules
mkdir -p $RPM_BUILD_ROOT%{_datadir}/hal/fdi/information/10freedesktop
install -p -m 644 libmtp.fdi $RPM_BUILD_ROOT%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi
# Install device permissions
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/console.perms.d/
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/security/console.perms.d/60-libmtp.perms
#-- FEDORA COPY

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}/html
mv -f %{buildroot}/%{_datadir}/doc/%{name}-%{version}/html/* %{buildroot}/%{_datadir}/doc/%{name}/html/

%clean 
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

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
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%config(noreplace) %{_sysconfdir}/security/console.perms.d/*
%config(noreplace) %{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi
%{_bindir}/*
