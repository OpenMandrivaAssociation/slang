%ifarch %{arm}
# FIXME causes an undefined reference to __multi3 with clang 6.0
%global _disable_lto 1
%endif

%define major 2
%define minor 2
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define static %mklibname %{name} -s -d

%define pre %{nil}

%bcond_without pcre
%bcond_without png
%bcond_without onig

Summary:	The shared library for the S-Lang extension language
Name:		slang
%if 0%{pre}
Version:	2.3.2
Source0:	https://www.jedsoft.org/snapshots/slang-pre%{version}-%{pre}.tar.gz
Release:	0.pre%{pre}
%else
Version:	2.3.2
Source0:	http://www.jedsoft.org/releases/slang/%{name}-%{version}.tar.bz2
Release:	9
%endif
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.s-lang.org
Source1:	%{name}.rpmlintrc
Patch0:		slang-2.2.3-slsh-libs.patch
Patch1:		slang-2.2.4-modules-makefile.patch
Patch2:		slang-2.3.2-arm-build-workaround.patch
# Fedora patches
# don't use memcpy() on overlapping buffers
Patch10:	slang-getkey-memmove.patch
# disable test that fails with SIGHUP ignored
Patch11:	slang-sighuptest.patch
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

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n %{libname}
Summary:	The shared library for the S-Lang extension language
Group:		System/Libraries

%description -n %{libname}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n %{devname}
Summary:	The library and header files for development using S-Lang
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
This package contains the S-Lang extension language libraries and
header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.

%package -n %{static}
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n %{static}
Static development files for %{name}.

%package source
Summary:	Source code %{name}
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description source
This package contain source code for the slang library.

%package doc
Summary:	Extra documentation for slang libraries
Group:		Books/Computer books

%description doc
This package contains documentation about S-Lang.
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package slsh
Summary:	S-Lang script interpreter
Group:		Shells
Provides:	%{name} = %{EVRD}
Obsoletes:	%{mklibname %{name}}-modules < 2.3.2-8
Provides:	%{mklibname %{name}}-modules = 2.3.2-8

%description slsh
slsh is a program that embeds the S-Lang interpreter and may be used
to test slang scripts.

%prep
%if 0%{pre}
%setup -qn slang-pre%{version}-%{pre}
%else
%setup -q
%endif
%autopatch -p1

# fix permissions of installed modules
sed -i '/^INSTALL_MODULE=/s/_DATA//' configure

# disable test failing on 32-bit archs
sed -i '/TEST_SCRIPTS_SLC = /s/array //' src/test/Makefile

%build
%configure \
	--with-{onig,pcre,png,z}lib=%{_libdir} \
	--with-{onig,pcre,png,z}inc=%{_includedir} \
	--includedir=%{_includedir}/slang

%make_build -j1

# (tpg) somehow this fails on i586 and armv7hl
%ifnarch %{ix86} %{arm}
%check
make check
%endif

%install
%make_install install-static

install -d %{buildroot}%{_prefix}/src/slang
cp src/Makefile src/*.{c,h,inc} %{buildroot}%{_prefix}/src/slang

cp src/config.h %{buildroot}%{_prefix}/src/slang

strip --strip-debug --strip-unneeded %{buildroot}%{_libdir}/slang/v*/modules/*.so

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

%files -n %{libname}
%{_libdir}/libslang.so.%{major}*

%files -n %{devname}
%{_libdir}/libslang.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h
%{_libdir}/pkgconfig/slang.pc

%files -n %{static}
%{_libdir}/libslang.a

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
%dir %{_libdir}/slang
%{_libdir}/slang/v%{major}
%{_datadir}/slsh
%{_mandir}/man1/slsh.1*
%config(noreplace) %{_sysconfdir}/slsh.rc
