%define	major	2
%define	minor	2
%define	modules	%{mklibname %{name}}-modules
%define	libname %mklibname %{name} %{major}
%define	devname %mklibname %{name} -d
%define	static	%mklibname %{name} -s -d

%bcond_without	pcre
%bcond_without	png
%bcond_with	onig
%bcond_without	dietlibc
%bcond_without	uclibc

Summary:	The shared library for the S-Lang extension language
Name:		slang
Version:	2.2.4
Release:	20
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.s-lang.org
Source0:	ftp://ftp.fu-berlin.de/pub/unix/misc/slang/v%{major}.%{minor}/slang-%{version}.tar.bz2
Source1:	%{name}.rpmlintrc
Patch5:		slang-2.2.4-slsh-makefile.patch
Patch6:		slang-2.2.4-modules-makefile.patch
Patch7:		slang-2.2.4-perms.patch
Patch8:		slang-2.2.4-no-rpath.patch
Patch9:		slang-2.2.4-aarch64.patch
BuildRequires:	pkgconfig(libpng)
BuildRequires:	libtool
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	onig-devel
%if %{with diet}
BuildRequires:	dietlibc-devel
%endif
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n	%{modules}
Summary:	Modules for the S-Lang extension language
Group:		Development/Other
Conflicts:	%{libname} < 2.2.4-3

%description -n	%{modules}
This package contains the main modules for the S-Lang extension language.

%package -n	%{libname}
Summary:	The shared library for the S-Lang extension language
Group:		System/Libraries
Requires:	%{modules} = %{EVRD}

%description -n	%{libname}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%if %{with uclibc}
%package -n	uclibc-%{libname}
Summary:	The shared library for the S-Lang extension language linked against uClibc
Group:		System/Libraries

%description -n	uclibc-%{libname}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n	uclibc-%{devname}
Summary:	The library and header files for development using S-Lang
Group:		Development/C
Provides:	uclibc-%{name}-devel = %{EVRD}
Requires:	uclibc-%{libname} = %{EVRD}
Requires:	%{devname} = %{EVRD}
Conflicts:	%{devname} < 2.2.4-18

%description -n	uclibc-%{devname}
This package contains the S-Lang extension language libraries and
header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.
%endif

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

%package	source
Summary:	Source code %{name}
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description	source
This package contain source code for the slang library.

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

%description	slsh
slsh is a program that embeds the S-Lang interpreter and may be used
to test slang scripts.

%prep
%setup -q
%patch5 -p1
%patch6 -p1
%patch7 -p1 -b .lib_exec~
%patch8 -p1 -b .norpath~
%patch9 -p1 -b .aarch~

%if %{with diet}
mkdir diet
cp -r autoconf configure doc demo mkfiles modules slang.lis slsh src utf8 changes.txt COPYING diet
%endif

%if %{with uclibc}
mkdir uclibc
cp -r autoconf configure doc demo mkfiles modules slang.lis slsh src utf8 changes.txt COPYING uclibc
%endif

%build
%if %{with diet}
pushd diet
./configure \
CC="diet gcc" CFLAGS="-Os -g"
make -C src/ static
popd
%endif

%if %{with uclibc}
pushd uclibc
%configure2_5x	--prefix=%{uclibc_root} \
		--libdir=%{uclibc_root}%{_libdir} \
		CC="%{uclibc_cc}" CFLAGS="%{uclibc_cflags}" LDFLAGS="%{ldflags} -Wl,-O2"
make -C src/ static $PWD/src/elfobjs/libslang.so.%{version}
popd
%endif

%configure	--with-{onig,pcre,png,z}lib=%{_libdir} \
		--with-{onig,pcre,png,z}inc=%{_includedir} \
		--includedir=%{_includedir}/slang

make

%check
make check

%install
%makeinstall_std install-static

%if %{with diet}
install -m644 diet/src/objs/libslang.a -D %{buildroot}%{_prefix}/lib/dietlibc/lib-%{_arch}/libslang.a
%endif

install -d %{buildroot}%{_prefix}/src/slang
cp src/Makefile src/*.{c,h,inc} %{buildroot}%{_prefix}/src/slang

%if !%{with uclibc}
cp src/config.h %{buildroot}%{_prefix}/src/slang
%else
cp uclibc/src/config.h %{buildroot}%{_prefix}/src/slang
install -m644 uclibc/src/objs/libslang.a -D %{buildroot}%{uclibc_root}%{_libdir}/libslang.a
cp -a uclibc/src/elfobjs/libslang.so* %{buildroot}%{uclibc_root}%{_libdir}
%endif

%files -n %{modules}
%dir %{_libdir}/slang
%{_libdir}/slang/v%{major}

%files -n %{libname}
%{_libdir}/libslang.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libslang.so.%{major}*

%files -n uclibc-%{devname}
%{uclibc_root}%{_libdir}/libslang.so
%{_prefix}/uclibc%{_libdir}/libslang.a
%endif

%files -n %{devname}
%{_libdir}/libslang.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h
%{_libdir}/pkgconfig/slang.pc

%files -n %{static}
%{_libdir}/libslang.a
%if %{with diet}
%{_prefix}/lib/dietlibc/lib-%{_arch}/libslang.a
%endif

%files source
%dir %{_prefix}/src/slang
%{_prefix}/src/slang/Makefile
%{_prefix}/src/slang/*.c
%{_prefix}/src/slang/*.h
%{_prefix}/src/slang/*.inc

%files doc
%{_defaultdocdir}/slang

%files slsh
%doc %{_docdir}/slsh
%{_bindir}/slsh
%{_datadir}/slsh
%{_mandir}/man1/slsh.1*
%config(noreplace) %{_sysconfdir}/slsh.rc
