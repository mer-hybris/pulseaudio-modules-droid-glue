%define pulseversion %{expand:%(rpm -q --qf '[%%{version}]' pulseaudio)}
%define pulsemajorminor %{expand:%(echo '%{pulseversion}' | cut -d+ -f1)}
%define moduleversion %{pulsemajorminor}.%{expand:%(echo '%{version}' | cut -d. -f3)}

Name:       pulseaudio-modules-droid-glue

Summary:    PulseAudio Droid HAL glue module
Version:    %{pulsemajorminor}.9
Release:    1
License:    LGPLv2+
URL:        https://github.com/mer-hybris/pulseaudio-modules-droid-glue
Source0:    %{name}-%{version}.tar.bz2
Requires:   pulseaudio >= %{pulseversion}
Requires:   audioflingerglue >= 0.0.1
Requires:   pulseaudio-modules-droid
BuildRequires:  libtool-ltdl-devel
BuildRequires:  meson
BuildRequires:  audioflingerglue-devel >= 0.0.1
BuildRequires:  pkgconfig(pulsecore) >= %{pulsemajorminor}
BuildRequires:  pkgconfig(android-headers)
BuildRequires:  pkgconfig(libhardware)

%description
PulseAudio Droid HAL glue module.


%prep
%autosetup -n %{name}-%{version}

%build
echo "%{moduleversion}" > .tarball-version
# Obtain the DEVICE from the same source as used in /etc/os-release
if [ -e "%{_includedir}/droid-devel/hw-release.vars" ]; then
. %{_includedir}/droid-devel/hw-release.vars
else
. %{_libdir}/droid-devel/hw-release.vars
fi

%meson -Ddroid-device=$MER_HA_DEVICE
%meson_build

%install
%meson_install

%files
%{_libdir}/pulse-*/modules/*.so
%license COPYING
