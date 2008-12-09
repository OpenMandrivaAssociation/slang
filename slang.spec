%define major 2
%define minor 1
%define	libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -s -d

%define with_pcre	1
%define with_png	1
%define with_onig	0

Summary:	The shared library for the S-Lang extension language
Name:		slang
Version:	2.1.4
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.s-lang.org
Source0:	ftp://space.mit.edu/pub/davis/slang/v%{major}.%{minor}/slang-%{version}.tar.bz2
Source1:	%{SOURCE0}.asc
# Do not use glibc private symbol (fedora bug #161536)
# See fedora package for a patch against newer slang
Patch0: 	slang-2.1.0-no_glibc_private.patch
Patch2:		slang-2.1.4-makefile.patch
Patch3:		slang-LANG.patch
Patch4:		slang-SLANG_LIB_FOR_MODULES.diff
BuildRequires:	glibc-devel
BuildRequires:	X11-devel
%if %{with_png}
BuildRequires:	libpng-devel
%endif
BuildRequires:	libtool
%if %{with_pcre}
BuildRequires:	pcre-devel
%endif
%if %{with_onig}
BuildRequires:	onig-devel
%endif
BuildConflicts:	slang-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Provides:	slang
Obsoletes:	slang < 2.1.4

%description -n	%{libname}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n %{develname}
Summary:	The library and header files for development using S-Lang
Group:		Development/C
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	slang-devel < 2.1.4
Obsoletes:	%{mklibname slang 2 -d}
Requires:	%{libname} = %{version}
Conflicts:	%{mklibname slang 1 -d}

%description -n	%{develname}
This package contains the S-Lang extension language libraries and
header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.

%package -n %{staticname}
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%{mklibname slang 2 -d -s}

%description -n %{staticname}
Static development files for %{name}.

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
Provides:	%{_bindir}/slsh

%description slsh
slsh is a program that embeds the S-Lang interpreter and may be used
to test slang scripts.

%prep

%setup -q
%patch0 -p1 -b .no_glibc_private
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure2_5x \
	--includedir=%{_includedir}/slang \
	%if %{with_onig}
	--with-onig \
	%endif
	%if %{with_png}
	--with-png \
	%endif
	%if %{with_pcre}
	--with-pcre
	%endif

%make static all

%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std DESTDIR=%{buildroot} install-static install

# Remove unwanted files
%if !%{with_pcre}
rm -f %{buildroot}%{_libdir}/slang/v%{major}/modules/pcre-module.so
%endif
%if !%{with_png}
rm -f %{buildroot}%{_libdir}/slang/v%{major}/modules/png-module.so
%endif
%if !%{with_onig}
rm -f %{buildroot}%{_libdir}/slang/v%{major}/modules/onig-module.so
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libslang.so.%{major}*
%dir %{_libdir}/slang
%{_libdir}/slang/v%{major}

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libslang.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/libslang.a

%files doc
%defattr(-,root,root)
%{_defaultdocdir}/slang

%files slsh
%defattr(-,root,root)
%doc %{_docdir}/slsh
%{_bindir}/slsh
%{_datadir}/slsh
%{_mandir}/man1/slsh.1*
%config %{_sysconfdir}/slsh.rc
