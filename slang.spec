%define docversion 1.4.8

%define major 1
%define	libname %mklibname %{name} %{major}

Summary:	The shared library for the S-Lang extension language
Name:		slang
Version:	1.4.9
Release:	%mkrel 10
License:	GPL
Group:		System/Libraries
URL:		ftp://space.mit.edu/pub/davis/slang/
Source0:	ftp://space.mit.edu/pub/davis/slang/slang-%{version}.tar.bz2
Source1:	ftp://space.mit.edu/pub/davis/slang/slang-%{docversion}-doc.tar.bz2
Source2:	README.UTF-8
# (mpol) utf8 patches from http://www.suse.de/~nadvornik/slang/
Patch1:		slang-debian-utf8.patch
Patch2:		slang-utf8-acs.patch
Patch3:		slang-utf8-fix.patch
Patch4:		slang-utf8-revert_soname.patch
Patch5:		slang-1.4.9-offbyone.patch
Patch12:	slang-1.4.5-utf8-segv.patch
Patch14:	slang-1.4.9-gcc4.patch
# Do not use glibc private symbol (fedora bug #161536)
# See fedora package for a patch against newer slang
Patch15:	slang-1.4.9-no-glibc-private.patch
BuildRequires:	libtool
BuildRequires:	autoconf2.5
Buildroot:	%{_tmppath}/slang-root

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n	%{libname}
Summary:	The shared library for the S-Lang extension language.
Group:		System/Libraries
Provides:	slang
Obsoletes:	slang

%description -n	%{libname}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n	%{libname}-devel
Summary:	The static library and header files for development using S-Lang.
Group:		Development/C
Provides:	lib%{name}-devel slang-devel
Obsoletes:	slang-devel
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
This package contains the S-Lang extension language static libraries
and header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.

%package	doc
Summary:	Extra documentation for slang libraries
Group:		Books/Computer books
Version:	%{docversion}

%description	doc
This package contains documentation about S-Lang.
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%prep

%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .revert_soname
%patch5 -p1 -b .offbyone

%patch12 -p1 -b .segv
%patch14 -p1 -b .gcc4

%patch15 -p1 -b .private

cp %{SOURCE2} .

%build

%configure2_5x	--includedir=%{_includedir}/slang

#(peroyvind) passing this to configure does'nt work..
%make ELF_CFLAGS="%{optflags} -fno-strength-reduce -fPIC" elf
%make all
cd doc && tar xjvf %{SOURCE1}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_includedir}/slang

make prefix=%{buildroot}%{_prefix} \
    install_lib_dir=%{buildroot}%{_libdir} \
    install_include_dir=%{buildroot}%{_includedir}/slang \
    install-elf install

ln -sf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}

rm -f doc/doc/tm/tools/`arch`objs doc/doc/tm/tools/solarisobjs

# Remove unpackages files
rm -rf	%{buildroot}/usr/doc/slang/COPYING \
	%{buildroot}/usr/doc/slang/COPYING.ART \
	%{buildroot}/usr/doc/slang/COPYING.GPL \
	%{buildroot}/usr/doc/slang/COPYRIGHT \
	%{buildroot}/usr/doc/slang/changes.txt \
	%{buildroot}/usr/doc/slang/cref.txt \
	%{buildroot}/usr/doc/slang/cslang.txt \
	%{buildroot}/usr/doc/slang/slang.txt \
	%{buildroot}/usr/doc/slang/slangdoc.html \
	%{buildroot}/usr/doc/slang/slangfun.txt

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libslang.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libslang.a
%{_libdir}/libslang.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h

%files doc
%defattr(-,root,root)
%doc doc COPYING COPYRIGHT README README.UTF-8 changes.txt NEWS 


