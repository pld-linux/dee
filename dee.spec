Summary:	Model to synchronize multiple instances over DBus
Name:		dee
Version:	1.0.14
Release:	2
# GPLv3-licensed tests and examples are in the tarball, but not installed
License:	LGPL v3
Group:		Libraries
URL:		https://launchpad.net/dee
Source0:	http://launchpad.net/dee/1.0/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	473b4181e26538af0fb753255da7945c
BuildRequires:	dbus-glib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	vala
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libdee is a library that uses DBus to provide objects allowing you to
create Model-View-Controller type programs across DBus. It also
consists of utility objects which extend DBus allowing for
peer-to-peer discoverability of known objects without needing a
central registrar.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation

%description apidocs
API and internal documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%package -n python-dee
Summary:	Python bindings for dee
Group:		Development/Languages/Python
Requires:	python-pygobject

%description -n python-dee
Python bindings for dee.

%prep
%setup -q

%build
%configure \
	--disable-static \
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
%attr(755,root,root) %{_bindir}/dee-tool
%{_libdir}/girepository-1.0/*.typelib
%attr(755,root,root) %{_libdir}/libdee-*.so.*.*.*
%ghost %{_libdir}/libdee-*.so.4

%files	devel
%defattr(644,root,root,755)
%{_includedir}/dee-1.0
%{_libdir}/libdee*.so
%{_pkgconfigdir}/*.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/*.vapi
%{_datadir}/vala/vapi/*.deps

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dee-1.0

%files -n python-dee
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Dee.py[co]
