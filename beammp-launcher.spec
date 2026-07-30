%global _binary_payload w22T0.zstdio

Name:           beammp-launcher
Version:        2.8.0
Release:        14%{?dist}
Summary:        Multiplayer Launcher/Client for BeamMP (BeamNG.drive)

License:        AGPL-3.0-only
URL:            https://github.com/BeamMP/BeamMP-Launcher
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/CoffeemanHell/beammp-copr/main/logo-white.png

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  ImageMagick
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
BuildRequires:  zlib-devel
BuildRequires:  nlohmann-json-devel
BuildRequires:  cpp-httplib-devel

Requires:       hicolor-icon-theme
Requires:       bash

%description
%{summary}
Native Linux launcher for BeamMP, the multiplayer mod for BeamNG.drive.

%prep
%autosetup -n BeamMP-Launcher-%{version}
sed -i 's/\r$//' README.md

%build
%cmake \
    -DCMAKE_C_FLAGS="%{optflags} -fPIC" \
    -DCMAKE_CXX_FLAGS="%{optflags} -fPIC" \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON

%cmake_build

%install
install -D -p -m 0755 %{_vpath_builddir}/BeamMP-Launcher %{buildroot}%{_libexecdir}/%{name}/BeamMP-Launcher

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/beammp-launcher << 'EOF'
#!/bin/bash
XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
BEAMMP_DIR="$XDG_DATA_HOME/BeamMP-Launcher"

mkdir -p "$BEAMMP_DIR/logs"
cd "$BEAMMP_DIR" || exit 1

ulimit -c 0

exec %{_libexecdir}/beammp-launcher/BeamMP-Launcher --no-update "$@"
EOF

chmod 0755 %{buildroot}%{_bindir}/beammp-launcher

mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/com.beammp.launcher.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Name=BeamMP
Comment=Multiplayer mod for BeamNG.drive
Exec=beammp-launcher
Icon=beammp-launcher
Terminal=false
Type=Application
Categories=Game;
StartupNotify=true
StartupWMClass=BeamMP-Launcher
EOF

mkdir -p %{buildroot}%{_metainfodir}
cat > %{buildroot}%{_metainfodir}/com.beammp.launcher.metainfo.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>com.beammp.launcher.desktop</id>
  <name>BeamMP</name>
  <summary>Multiplayer Launcher for BeamMP (BeamNG.drive)</summary>
  <metadata_license>FSFAP</metadata_license>
  <project_license>AGPL-3.0-only</project_license>
  <description>
    <p>Native Linux launcher for BeamMP, the multiplayer mod for BeamNG.drive.</p>
  </description>
  <launchable type="desktop-id">com.beammp.launcher.desktop</launchable>
  <url type="homepage">https://beammp.com</url>
  <url type="bugtracker">https://github.com/BeamMP/BeamMP-Launcher/issues</url>
</component>
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/
magick %{SOURCE1} -resize 512x512 -strip \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/beammp-launcher.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.beammp.launcher.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.beammp.launcher.metainfo.xml

%files
%license LICENSE
%doc README.md
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/BeamMP-Launcher
%{_bindir}/beammp-launcher
%{_datadir}/applications/com.beammp.launcher.desktop
%{_metainfodir}/com.beammp.launcher.metainfo.xml
%{_datadir}/icons/hicolor/512x512/apps/beammp-launcher.png

%changelog
* Sat Jul 18 2026 coffeeicus <coffeelover@coffeelover.uk> - 2.8.0-14
- Switch to native system libraries instead of bundled vcpkg.
