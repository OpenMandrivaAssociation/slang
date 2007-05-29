%define major 2
%define minor 1
%define	libname %mklibname %{name} %{major}

%define with_pcre 1
%define with_png 1

Summary:	The shared library for the S-Lang extension language
Name:		slang
Version:	%{major}.%{minor}.0
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
URL:		http://www.s-lang.org
Source0:	ftp://space.mit.edu/pub/davis/slang/v%{major}.%{minor}/slang-%{version}.tar.bz2
Source1:	ftp://space.mit.edu/pub/davis/slang/v%{major}.%{minor}/slang-%{version}.tar.bz2.sig
# Do not use glibc private symbol (fedora bug #161536)
# See fedora package for a patch against newer slang
Patch0: 	slang-2.1.0-no_glibc_private.patch
# Fix install of slsh when slang 1 is installed on the system
Patch1: 	slang-2.1.0-slsh_install.patch

BuildRequires:	glibc-devel
%if %{with_png}
BuildRequires:	libpng-devel
%endif
BuildRequires:	libtool
%if %{with_pcre}
BuildRequires:	pcre-devel
%endif

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
Summary:	The library and header files for development using S-Lang
Group:		Development/C
Provides:	lib%{name}-devel slang-devel
Obsoletes:	slang-devel
Requires:	%{libname} = %{version}
Conflicts:	libslang1-devel

%description -n	%{libname}-devel
This package contains the S-Lang extension language libraries and
header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.

%package -n %{libname}-static-devel
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel slang-static-devel

%description -n %{libname}-static-devel
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

%description slsh
slsh is a program that embeds the S-Lang interpreter and may be used
to test slang scripts.

%prep
%setup -q
%patch0 -p1 -b .no_glibc_private
%patch1 -p1 -b .slsh_install

%build
%configure --includedir=%{_includedir}/slang
make static all
make check

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install-static install

# Remove unwanted files
%if !%{with_pcre}
rm -f %{buildroot}%{_libdir}/slang/v%{major}/modules/pcre-module.so
%endif
%if !%{with_png}
rm -f %{buildroot}%{_libdir}/slang/v%{major}/modules/png-module.so
%endif

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libslang.so.%{major}*
%dir %{_libdir}/slang
%{_libdir}/slang/v%{major}

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libslang.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/libslang.a

%files doc
%defattr(-,root,root)
%{_defaultdocdir}/slang

%files slsh
%defattr(-,root,root)
%{_bindir}/slsh
%{_datadir}/slsh
%{_mandir}/man1/slsh.1*
%config %{_sysconfdir}/slsh.rc
