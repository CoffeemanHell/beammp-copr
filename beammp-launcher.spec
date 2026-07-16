Name:           beammp-launcher
Version:        2.8.0
Release:        2%{?dist}
Summary:        Multiplayer Launcher/Client for BeamMP (BeamNG.drive)

License:        AGPL-3.0-only
URL:            https://github.com/BeamMP/BeamMP-Launcher

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

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

cmake . -B bin \
    -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake \
    -DVCPKG_TARGET_TRIPLET=x64-linux

cmake --build bin %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libexecdir}
install -m 755 bin/BeamMP-Launcher %{buildroot}%{_libexecdir}/BeamMP-Launcher-bin

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/beammp-launcher << 'EOF'

LAUNCHER_DIR="$HOME/beammp-launcher"

mkdir -p "$LAUNCHER_DIR"

if [ ! -f "$LAUNCHER_DIR/BeamMP-Launcher" ] || [ /usr/libexec/BeamMP-Launcher-bin -nt "$LAUNCHER_DIR/BeamMP-Launcher" ]; then
    echo "[BeamMP Wrapper] Preparing files..."
    cp /usr/libexec/BeamMP-Launcher-bin "$LAUNCHER_DIR/BeamMP-Launcher"
    chmod +x "$LAUNCHER_DIR/BeamMP-Launcher"
fi

cd "$LAUNCHER_DIR" || exit 1
exec ./BeamMP-Launcher "$@"
EOF

chmod 755 %{buildroot}%{_bindir}/beammp-launcher

mkdir -p "%{buildroot}%{_datadir}/applications/"
cat > "%{buildroot}%{_datadir}/applications/com.beammp.launcher.desktop" << 'EOF'
[Desktop Entry]
Name=BeamMP
Comment=Multiplayer mod for BeamNG.drive
Exec=beammp-launcher
Terminal=true
Type=Application
Categories=Game;
EOF

%files
%{_libexecdir}/BeamMP-Launcher-bin
%{_bindir}/beammp-launcher
%{_datadir}/applications/com.beammp.launcher.desktop
%license LICENSE
%doc README.md

%changelog
* Thu Jul 16 2026 coffeeicus <coffeelover@coffeelover.uk> - 2.8.0-2
