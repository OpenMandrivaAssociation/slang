%define	major	2
%define	minor	2
%define	modules	%{mklibname %{name}}-modules
%define	libname %mklibname %{name} %{major}
%define	devname %mklibname %{name} -d
%define	static	%mklibname %{name} -s -d

%bcond_without	pcre
%bcond_without	png
%bcond_without	onig
%bcond_without	dietlibc
%bcond_with	uclibc

Summary:	The shared library for the S-Lang extension language
Name:		slang
Version:	2.3.1a
Release:	1
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.s-lang.org
Source0:	http://www.jedsoft.org/releases/slang/%{name}-%{version}.tar.bz2
Source1:	%{name}.rpmlintrc
Patch0:		slang-2.3.1a-slsh-libs.patch
Patch1:		slang-2.3.1a-modules-makefile.patch
Patch2:		slang-2.2.4-perms.patch
Patch3:		slang-2.2.4-drop-inline-for-fwhole-program-usage-elsewhere.patch
BuildRequires:	pkgconfig(libpng)
BuildRequires:	libtool
BuildRequires:	readline-devel
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
%patch0 -p1 -b .slsh~
%patch1 -p1 -b .modules~
%patch2 -p1 -b .perms~

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
%uclibc_configure --with-readline=gnu
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
install -m644 diet/src/config.h -D %{buildroot}%{_usrsrc}/slang/config-diet.h
%endif

install -d %{buildroot}%{_usrsrc}/slang
cp src/Makefile src/*.{c,h,inc} %{buildroot}%{_usrsrc}/slang
pushd %{buildroot}%{_usrsrc}/slang
patch -i %{PATCH3} -p2
popd

cp src/config.h %{buildroot}%{_usrsrc}/slang/config-glibc.h
%if %{with uclibc}
cp uclibc/src/config.h %{buildroot}%{_usrsrc}/slang/config-uclibc.h
install -m644 uclibc/src/objs/libslang.a -D %{buildroot}%{uclibc_root}%{_libdir}/libslang.a
cp -a uclibc/src/elfobjs/libslang.so* %{buildroot}%{uclibc_root}%{_libdir}
%endif
cat > %{buildroot}%{_usrsrc}/slang/config.h <<EOF
#include <features.h>
#if defined(__UCLIBC__)
#include "config-uclibc.h"
#elif defined(__dietlibc__)
#include "config-diet.h"
#elif defined(__GLIBC__)
#include "config-glibc.h"
#endif
EOF

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
%dir %{_usrsrc}/slang
%{_usrsrc}/slang/Makefile
%{_usrsrc}/slang/*.c
%{_usrsrc}/slang/*.h
%{_usrsrc}/slang/*.inc

%files doc
%{_defaultdocdir}/slang

%files slsh
%doc %{_docdir}/slsh
%{_bindir}/slsh
%{_datadir}/slsh
%{_mandir}/man1/slsh.1*
%config(noreplace) %{_sysconfdir}/slsh.rc
