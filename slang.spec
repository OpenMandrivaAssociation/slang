%define	major	2
%define	minor	2
%define	libname %mklibname %{name} %{major}
%define	devname %mklibname %{name} -d
%define	static	%mklibname %{name} -s -d

%bcond_without	pcre
%bcond_without	png
%bcond_with	onig

Summary:	The shared library for the S-Lang extension language
Name:		slang
Version:	2.2.4
Release:	3
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.s-lang.org
Source0:	ftp://ftp.fu-berlin.de/pub/unix/misc/slang/v%{major}.%{minor}/slang-%{version}.tar.bz2
Source1:	%{SOURCE0}.asc
Patch5:		slang-2.2.4-slsh-makefile.patch
Patch6:		slang-2.2.4-modules-makefile.patch
Patch7:		slang-2.2.4-perms.patch
%if %{with png}
BuildRequires:	libpng-devel
%endif
BuildRequires:	libtool
%if %{with pcre}
BuildRequires:	pcre-devel
%endif
%if %{with onig}
BuildRequires:	onig-devel
%endif

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n	%{libname}
Summary:	The shared library for the S-Lang extension language
Group:		System/Libraries

%description -n	%{libname}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n	%{devname}
Summary:	The library and header files for development using S-Lang
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
This package contains the S-Lang extension language libraries and
header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.

%package -n	%{static}
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n	%{static}
Static development files for %{name}.

%package	doc
Summary:	Extra documentation for slang libraries
Group:		Books/Computer books

%description	doc
This package contains documentation about S-Lang.
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package	slsh
Summary:	S-Lang script interpreter
Group:		Shells
Provides:	%{_bindir}/slsh

%description	slsh
slsh is a program that embeds the S-Lang interpreter and may be used
to test slang scripts.

%prep
%setup -q
%patch5 -p1
%patch6 -p1
%patch7 -p1 -b .lib_exec~

%build
%configure2_5x	--includedir=%{_includedir}/slang \
%if %{with onig}
		--with-onig \
%else
		--without-onig \
%endif
%if %{with png}
		--with-png \
%else
		--without-png \
%endif
%if %{with pcre}
		--with-pcre
%else
		--without-pcre
%endif

%make

%check
make check

%install
%makeinstall_std install-static

%files -n %{libname}
%{_libdir}/libslang.so.%{major}*
%dir %{_libdir}/slang
%{_libdir}/slang/v%{major}

%files -n %{devname}
%{_libdir}/libslang.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h
%{_libdir}/pkgconfig/slang.pc

%files -n %{static}
%{_libdir}/libslang.a

%files doc
%{_defaultdocdir}/slang

%files slsh
%doc %{_docdir}/slsh
%{_bindir}/slsh
%{_datadir}/slsh
%{_mandir}/man1/slsh.1*
%config %{_sysconfdir}/slsh.rc
