%global _binary_payload w22T0.zstdio

Name:           beammp-launcher
Version:        2.8.0
Release:        6%{?dist}
Summary:        Multiplayer Launcher/Client for BeamMP (BeamNG.drive)

License:        AGPL-3.0-only
URL:            https://github.com/BeamMP/BeamMP-Launcher
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/BeamMP/Wiki/main/logo.png

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-IPC-Cmd
BuildRequires:  perl-FindBin
BuildRequires:  perl-File-Compare
BuildRequires:  perl-File-Copy
BuildRequires:  kernel-headers
BuildRequires:  kernel-devel
BuildRequires:  git
BuildRequires:  curl
BuildRequires:  zip
BuildRequires:  unzip
BuildRequires:  tar
BuildRequires:  desktop-file-utils

%global debug_package %{nil}

%description
BeamMP Launcher

%prep
%autosetup -n BeamMP-Launcher-%{version}

git clone https://github.com/microsoft/vcpkg.git vcpkg
cd vcpkg
./bootstrap-vcpkg.sh -disableMetrics
cd ..

%build
export VCPKG_ROOT="$(pwd)/vcpkg"
export PATH=$VCPKG_ROOT:$PATH

export CFLAGS="-O3 -march=x86-64-v3 -pipe -fPIC -fexceptions -fstack-protector-strong"
export CXXFLAGS="-O3 -march=x86-64-v3 -pipe -fPIC -fexceptions -fstack-protector-strong"
export VCPKG_KEEP_ENV_VARS="CFLAGS;CXXFLAGS"

cmake . -B bin \
    -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake \
    -DVCPKG_TARGET_TRIPLET=x64-linux \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DCMAKE_C_FLAGS="$CFLAGS" \
    -DCMAKE_CXX_FLAGS="$CXXFLAGS"

cmake --build bin %{?_smp_mflags}

%install
install -D -p -m 0755 bin/BeamMP-Launcher %{buildroot}%{_libexecdir}/%{name}/BeamMP-Launcher

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/beammp-launcher << 'EOF'
#!/bin/bash
XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
BEAMMP_DIR="$XDG_DATA_HOME/BeamMP-Launcher"

mkdir -p "$BEAMMP_DIR"
cd "$BEAMMP_DIR" || exit 1

exec %{_libexecdir}/beammp-launcher/BeamMP-Launcher "$@"
EOF

chmod 0755 %{buildroot}%{_bindir}/beammp-launcher

mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/com.beammp.launcher.desktop << 'EOF'
[Desktop Entry]
Name=BeamMP
Comment=Multiplayer mod for BeamNG.drive
Exec=beammp-launcher
Icon=beammp-launcher
Terminal=false
Type=Application
Categories=Game;
EOF

install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/beammp-launcher.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.beammp.launcher.desktop

%files
%dir %{_libexecdir}/%{name}
%attr(0755, root, root) %{_libexecdir}/%{name}/BeamMP-Launcher
%attr(0755, root, root) %{_bindir}/beammp-launcher
%{_datadir}/applications/com.beammp.launcher.desktop
%{_datadir}/icons/hicolor/512x512/apps/beammp-launcher.png
%license LICENSE
%doc README.md

%changelog
* Thu Jul 16 2026 coffeeicus <coffeelover@coffeelover.uk> - 2.8.0-6
- Initial release.
