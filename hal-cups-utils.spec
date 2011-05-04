Summary:	A CUPS backend for HAL
Name:		hal-cups-utils
Version:	0.6.16
Release:	%mkrel 23
License:	GPLv2+
Group:		System/Configuration/Printing
URL:		https://fedorahosted.org/hal-cups-utils/
Source:		https://fedorahosted.org/releases/h/a/hal-cups-utils/%{name}-%{version}.tar.bz2
Source1:	mdv_printer_custom.py
Source2:    hp-makeuri-mdv.c
Source3:    mdv_backend
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	dbus-glib-devel
BuildRequires:  libcups-devel
BuildRequires:  libhal-devel
BuildRequires:  python-devel
BuildRequires:  libhpip-devel
Requires:   hplip-model-data
# nmap is required to scan the network, just like 
# printerdrake used to do.
Requires:   nmap
Patch1:		hal-cups-utils-0.6.16-svn.patch
Patch2:		hal-cups-utils-0.6.16-nocupsinclude.patch
Patch3:		hal-cups-utils-0.6.16-fixlibdir.patch
Patch4:		hal-cups-utils-0.6.16-mdv_custom.patch

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
%patch4 -p1 -b .mdv_custom

%build
./autogen.sh
%configure2_5x
%make
# (salem) this hack avoids requiring hplip
gcc %{SOURCE2} -o hp-makeuri-mdv -lhpmud

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mozillaextpath}
mkdir -p %{buildroot}%{py_platsitedir}
mkdir -p %{buildroot}%{_bindir}
cp -f %{SOURCE1} %{buildroot}%{py_platsitedir}
cp -f hp-makeuri-mdv %{buildroot}%{_bindir}

%makeinstall_std

cp -f %{SOURCE3} %{buildroot}%{_libdir}/cups/backend

# Make cups run this backend as root to workaround device permissions issues (bug #49407)
chmod 0700 %{buildroot}%{_libdir}/cups/backend/hal

mkdir -p %{buildroot}%{_libdir}/hal
mv  %{buildroot}%{_libdir}/hal_lpadmin %{buildroot}%{_libdir}/hal
pushd %{buildroot}%{py_platsitedir}
python -m compileall .
popd

%find_lang %name

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc INSTALL README NEWS ChangeLog
%{_libdir}/cups/backend/hal
%{_libdir}/cups/backend/mdv_backend
%{_libdir}/hal/hal_lpadmin
%{_bindir}/hp-makeuri-mdv
%{_datadir}/hal/fdi/policy/10osvendor/10-hal_lpadmin.fdi
%{py_platsitedir}/mdv_printer_custom.py*

%post
# disable old printer detection system
if [ -f /etc/sysconfig/printing ]; then
    if grep -q ^AUTO_SETUP_QUEUES_ON_PRINTER_CONNECTED= /etc/sysconfig/printing; then
        sed -i 's/AUTO_SETUP_QUEUES_ON_PRINTER_CONNECTED=.*/AUTO_SETUP_QUEUES_ON_PRINTER_CONNECTED=no/g' /etc/sysconfig/printing
    else
        echo AUTO_SETUP_QUEUES_ON_PRINTER_CONNECTED=no >> /etc/sysconfig/printing
    fi
    if grep -q ^ENABLE_QUEUES_ON_PRINTER_CONNECTED= /etc/sysconfig/printing; then
        sed -i 's/ENABLE_QUEUES_ON_PRINTER_CONNECTED=.*/ENABLE_QUEUES_ON_PRINTER_CONNECTED=no/g' /etc/sysconfig/printing
    else
        echo ENABLE_QUEUES_ON_PRINTER_CONNECTED=no >> /etc/sysconfig/printing
    fi
else
    echo AUTO_SETUP_QUEUES_ON_PRINTER_CONNECTED=no >> /etc/sysconfig/printing
    echo ENABLE_QUEUES_ON_PRINTER_CONNECTED=no >> /etc/sysconfig/printing
fi

%postun
# enable old printer detection system
if [ -f /etc/sysconfig/printing ]; then
    if grep -q ^AUTO_SETUP_QUEUES_ON_PRINTER_CONNECTED= /etc/sysconfig/printing; then
        sed -i 's/AUTO_SETUP_QUEUES_ON_PRINTER_CONNECTED=.*/AUTO_SETUP_QUEUES_ON_PRINTER_CONNECTED=yes/g' /etc/sysconfig/printing
    fi
    if grep -q ^ENABLE_QUEUES_ON_PRINTER_CONNECTED= /etc/sysconfig/printing; then
        sed -i 's/ENABLE_QUEUES_ON_PRINTER_CONNECTED=.*/ENABLE_QUEUES_ON_PRINTER_CONNECTED=yes/g' /etc/sysconfig/printing
    fi
fi

