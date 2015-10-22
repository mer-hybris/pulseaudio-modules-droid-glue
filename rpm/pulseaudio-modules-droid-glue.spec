%define pulseversion %{expand:%(rpm -q --qf '[%%{version}]' pulseaudio)}
%define pulsemajorminor %{expand:%(echo '%{pulseversion}' | cut -d+ -f1)}
%define moduleversion %{pulsemajorminor}.%{expand:%(echo '%{version}' | cut -d. -f3)}

Name:       pulseaudio-modules-droid-glue

Summary:    PulseAudio Droid HAL glue module
Version:    %{pulsemajorminor}.1
Release:    1
Group:      Multimedia/PulseAudio
License:    LGPLv2.1+
URL:        https://github.com/mer-hybris/pulseaudio-modules-droid-glue
Source0:    %{name}-%{version}.tar.bz2
Requires:   pulseaudio >= %{pulseversion}
Requires:   audioflingerglue >= 0.0.1
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libtool-ltdl-devel
BuildRequires:  audioflingerglue-devel >= 0.0.1
BuildRequires:  pkgconfig(pulsecore) >= %{pulsemajorminor}
BuildRequires:  pkgconfig(android-headers)
BuildRequires:  pkgconfig(libhardware)
BuildRequires:  pkgconfig(libdroid-util) >= %{pulsemajorminor}.41

%description
PulseAudio Droid HAL glue module.


%prep
%setup -q -n %{name}-%{version}

%build
echo "%{moduleversion}" > .tarball-version
# Obtain the DEVICE from the same source as used in /etc/os-release
. /usr/lib/droid-devel/hw-release.vars
%reconfigure --disable-static --with-droid-device=$MER_HA_DEVICE
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%files
%defattr(-,root,root,-)
%{_libdir}/pulse-%{pulsemajorminor}/modules/*.so
