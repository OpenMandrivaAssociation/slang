%define	major 2
%define	minor 2
%define	modules	%{mklibname %{name}}-modules
%define	libname %mklibname %{name} %{major}
%define	devname %mklibname %{name} -d
%define	static	%mklibname %{name} -s -d

%define pre %{nil}

%bcond_without	pcre
%bcond_without	png
%bcond_without	onig
%bcond_without	dietlibc

Summary:	The shared library for the S-Lang extension language
Name:		slang
%if 0%{pre}
Version:	2.3.2
Source0:	https://www.jedsoft.org/snapshots/slang-pre%{version}-%{pre}.tar.gz
Release:	0.pre%{pre}
%else
Version:	2.3.2
Source0:	http://www.jedsoft.org/releases/slang/%{name}-%{version}.tar.bz2
Release:	1
%endif
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.s-lang.org
Source1:	%{name}.rpmlintrc
Patch0:		slang-2.2.3-slsh-libs.patch
Patch1:		slang-2.2.4-modules-makefile.patch
BuildRequires:	libtool
%if %{with png}
BuildRequires:	pkgconfig(libpng)
%endif
%if %{with pcre}
BuildRequires:	pkgconfig(libpcre)
%endif
%if %{with onig}
BuildRequires:	onig-devel
%endif
%if %{with diet}
BuildRequires:	dietlibc-devel
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
%if 0%{pre}
%setup -qn slang-pre%{version}-%{pre}
%else
%setup -q
%endif
%apply_patches

%if %{with diet}
mkdir diet
cp -r autoconf configure doc demo mkfiles modules slang.lis slsh src utf8 changes.txt COPYING diet
%endif

%build
%if %{with diet}
pushd diet
./configure \
CC="diet gcc" CFLAGS="-Os -g"
%make -j1 -C src/ static
popd
%endif

%configure \
	--with-{onig,pcre,png,z}lib=%{_libdir} \
	--with-{onig,pcre,png,z}inc=%{_includedir} \
	--includedir=%{_includedir}/slang

%make -j1

# (tpg) somehow this fails on i586
%ifnarch %{ix86}
%check
make check
%endif

%install
%makeinstall_std install-static

%if %{with diet}
install -m644 diet/src/objs/libslang.a -D %{buildroot}%{_prefix}/lib/dietlibc/lib-%{_arch}/libslang.a
%endif

install -d %{buildroot}%{_prefix}/src/slang
cp src/Makefile src/*.{c,h,inc} %{buildroot}%{_prefix}/src/slang

cp src/config.h %{buildroot}%{_prefix}/src/slang

%files -n %{modules}
%dir %{_libdir}/slang
%{_libdir}/slang/v%{major}

%files -n %{libname}
%{_libdir}/libslang.so.%{major}*

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
