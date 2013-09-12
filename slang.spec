%define	major	2
%define	minor	2
%define	modules	%{mklibname %{name}}-modules
%define	libname %mklibname %{name} %{major}
%define	devname %mklibname %{name} -d
%define	static	%mklibname %{name} -s -d

%bcond_without	pcre
%bcond_without	png
%bcond_without	onig
%bcond_without	diet
%bcond_without	uclibc

Summary:	The shared library for the S-Lang extension language
Name:		slang
Version:	2.2.4
Release:	11
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.s-lang.org
Source0:	ftp://ftp.fu-berlin.de/pub/unix/misc/slang/v%{major}.%{minor}/slang-%{version}.tar.bz2
Patch5:		slang-2.2.4-slsh-makefile.patch
Patch6:		slang-2.2.4-modules-makefile.patch
Patch7:		slang-2.2.4-perms.patch
Patch8:		slang-2.2.4-no-rpath.patch
Patch9:		slang-2.2.4-drop-inline-for-fwhole-program-usage-elsewhere.patch
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
%endif

%package -n	%{devname}
Summary:	The library and header files for development using S-Lang
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}
%endif

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

%configure2_5x	--with-readline=gnu \
%if %{with pcre}
		--with-pcrelib=%{_libdir} \
		--with-pcreinc=%{_includedir} \
%endif
%if %{with png}
		--with-pnglib=%{_libdir} \
		--with-pnginc=%{_includedir} \
%endif
%if %{with onig}
		--with-oniglib=%{_libdir} \
		--with-oniginc=%{_includedir} \
%endif
		--with-zlib=%{_libdir} \
		--with-zinc=%{_includedir} \
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
pushd %{buildroot}%{_prefix}/src/slang
%patch9 -p2
popd

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
%endif

%files -n %{devname}
%{_libdir}/libslang.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libslang.so
%endif
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h
%{_libdir}/pkgconfig/slang.pc

%files -n %{static}
%{_libdir}/libslang.a
%if %{with diet}
%{_prefix}/lib/dietlibc/lib-%{_arch}/libslang.a
%endif
%if %{with uclibc}
%{_prefix}/uclibc%{_libdir}/libslang.a
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

%changelog
* Wed Dec 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.4-9
- rebuild on ABF

* Sun Oct 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.4-8
+ Revision: 820096
- add dependency on uclibc library package for devel package
- create a slang-source package with the source made available for others
  packages to compile it in with -fwhole-program
- build against latest uClibc for locale support

* Wed Jun 06 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.4-6
+ Revision: 802829
- drop unused %%{_bindir}/slsh provides
- fix linking against uclibc

* Wed Jun 06 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.4-5
+ Revision: 802824
- build uclibc dynamically linked version of library

* Thu May 24 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.4-4
+ Revision: 800342
- add conditional buildrequires on dietlibc-devel & uClibc-devel
- build static library version against uclibc & diet

* Wed Mar 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.4-3
+ Revision: 782937
- parallel build seems flakey, disable it for now..
- fix conffile-without-noreplace-flag
- split out modules into separate package
- use pkgconfig() deps for buildrequires
- fix build of libpng, libpcre, libonig & libz module & enable unconditionally
- get rid of rpath (P8)
- install libraries with executable permissions (P7, from Fedora)
- use %%{EVRD} macro
- drop ancient obsoletes
- drop excessive provides
- remove buildconflicts on slang-devel
- cleanups

* Tue Feb 07 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 2.2.4-2
+ Revision: 771692
- rebuild for new pcre

* Tue Sep 13 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2.2.4-1
+ Revision: 699605
- update to new version 2.2.4
- drop old pacthes
- Patch 5 and 6 : link against source slang library
- disable parallel build

  + Lonyai Gergely <aleph@mandriva.org>
    - rebuild

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.2-3
+ Revision: 669985
- mass rebuild

  + Funda Wang <fwang@mandriva.org>
    - tighten BR

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.2-2mdv2011.0
+ Revision: 607541
- rebuild

* Thu Dec 31 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.2.2-1mdv2010.1
+ Revision: 484500
- update to new version 2.2.2
- drop patch 3, fixed upstream
- rediff patch 2

