Summary:	A CUPS backend for HAL
Name:		hal-cups-utils
Version:	0.6.16
Release:	%mkrel 2
License:	GPLv2+
Group:		System/Configuration/Printing
URL:		http://svn.fedorahosted.org/svn/hal-cups-utils/tags/0.6.16/
Source:		%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	dbus-glib-devel
BuildRequires:  libcups-devel
BuildRequires:  libhal-devel
Patch1:		hal-cups-utils-0.6.16-svn.patch
Patch2:		hal-cups-utils-0.6.16-nocupsinclude.patch
Patch3:		hal-cups-utils-0.6.16-fixlibdir.patch

%description
This package contains utilities for linking CUPS to HAL. This includes:

* backend/hal - the CUPS backend for browsing local printers using HAL
* systemv/hal_lpadmin - a utility based on lpadmin for adding, configuring and
  removing printers using hal UDI's
* requires system-config-printer-libs and a running cups server

%prep
%setup -q
%patch1 -p1 -b .svnpatch
%patch2 -p1 -b .nocupsinclude
%patch3 -p1 -b .fixlibdir

%build
./autogen.sh
%configure2_5x
%make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mozillaextpath}

%makeinstall_std

%find_lang %name

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc INSTALL README NEWS ChangeLog
%{_libdir}/cups/backend/hal
%{_libdir}/hal_lpadmin
%{_datadir}/hal/fdi/policy/10osvendor/10-hal_lpadmin.fdi
