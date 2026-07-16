Name:           beammp-launcher
Version:        2.8.0
Release:        1%{?dist}
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
mkdir -p %{buildroot}%{_bindir}
install -m 755 bin/BeamMP-Launcher %{buildroot}%{_bindir}/beammp-launcher

%files
%{_bindir}/beammp-launcher
%license LICENSE
%doc README.md

%changelog
* Thu Jul 16 2026 coffeeicus <coffeelover@coffeelover.uk> - 2.8.0-1
- Initial release.
