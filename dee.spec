#
# Conditional build:
%bcond_without	static_libs	# static library build

Summary:	Model to synchronize multiple instances over DBus
Summary(pl.UTF-8):	Model synchronizacji wielu instancji poprzez DBus
Name:		dee
Version:	1.2.7
Release:	11
# GPLv3-licensed tests and examples are in the tarball, but not installed
License:	LGPL v3
Group:		Libraries
Source0:	http://launchpad.net/dee/1.0/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	b92f27f0a99cac24c2128880601bb7d7
Patch0:		no-Werror.patch
Patch1:		vapi-skip-properties.patch
Patch2:		dee-1.2.7-fix-duplicates-vala-0.5X.patch
URL:		https://launchpad.net/dee
BuildRequires:	glib2-devel >= 1:2.32
BuildRequires:	gobject-introspection-devel >= 0.10.2
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	libicu-devel >= 4.6
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.219
# not needed for releases
#BuildRequires:	vala
Requires:	glib2 >= 1:2.32
Requires:	libicu >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libdee is a library that uses DBus to provide objects allowing you to
create Model-View-Controller type programs across DBus. It also
consists of utility objects which extend DBus allowing for
peer-to-peer discoverability of known objects without needing a
central registrar.

%description -l pl.UTF-8
Libdee to biblioteka wykorzystująca DBus w celu zapewnienia obiektów
pozwalających na tworzenie programów typu model-widok-kontroler
poprzez DBus. Składa się z obiektów narzędziowych rozszerzających DBus
o możliwość widzenia znanych obiektów w komunikacji peer-to-peer bez
potrzeby centralnego rejestru.

%package devel
Summary:	Development files for libdee
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libdee
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32
Requires:	libicu-devel >= 4.6

%description devel
This package contains the header files for developing applications
that use libdee library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia aplikacji
wykorzystujących bibliotekę libdee.

%package static
Summary:	Static libdee library
Summary(pl.UTF-8):	Biblioteka statyczna libdee
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libdee library.

%description static -l pl.UTF-8
Biblioteka statyczna libdee.

%package apidocs
Summary:	Libdee API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libdee
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libdee library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libdee.

%package -n python-dee
Summary:	Python bindings for libdee
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libdee
Group:		Development/Languages/Python
Requires:	python-pygobject3

%description -n python-dee
Python bindings for libdee.

%description -n python-dee -l pl.UTF-8
Wiązania Pythona do biblioteki libdee.

%package -n vala-dee
Summary:	Libdee API for Vala language
Summary(pl.UTF-8):	API libdee dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-dee
Libdee API for Vala language.

%description -n vala-dee -l pl.UTF-8
API libdee dla języka Vala.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_gtkdocdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdee*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/dee-tool
%attr(755,root,root) %{_libdir}/libdee-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdee-1.0.so.4
%{_libdir}/girepository-1.0/Dee-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdee-1.0.so
%{_includedir}/dee-1.0
%{_pkgconfigdir}/dee-1.0.pc
%{_pkgconfigdir}/dee-icu-1.0.pc
%{_datadir}/gir-1.0/Dee-1.0.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdee-1.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dee-1.0

%files -n python-dee
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Dee.py[co]

%files -n vala-dee
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/dee-1.0.vapi
%{_datadir}/vala/vapi/dee-1.0.deps
