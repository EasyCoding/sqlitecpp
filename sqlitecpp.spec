%global richname SQLiteCpp

Name: sqlitecpp
Version: 2.4.0
Release: 2%{?dist}

License: MIT
Summary: Smart and easy to use C++ SQLite3 wrapper
URL: https://github.com/SRombauts/%{richname}
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# https://github.com/SRombauts/SQLiteCpp/pull/229
Patch0: %{name}-system-sqlite.patch
# https://github.com/SRombauts/SQLiteCpp/pull/230
Patch1: %{name}-fix-installation.patch
# https://github.com/SRombauts/SQLiteCpp/pull/231
Patch2: %{name}-add-soversion.patch
# https://github.com/SRombauts/SQLiteCpp/pull/232
Patch3: %{name}-system-gtest.patch

BuildRequires: sqlite-devel
BuildRequires: gtest-devel
BuildRequires: gmock-devel
BuildRequires: ninja-build
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc

%description
SQLiteC++ (SQLiteCpp) is a smart and easy to use C++ SQLite3 wrapper.

SQLiteC++ offers an encapsulation around the native C APIs of SQLite,
with a few intuitive and well documented C++ classes.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{richname}-%{version} -p1
mkdir -p %{_target_platform}

# Fixing W: wrong-file-end-of-line-encoding...
sed -e "s,\r,," -i README.md

# Removing bundled libraries...
rm -rf sqlite3
rm -rf googletest

%build
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DSQLITECPP_INTERNAL_SQLITE=OFF \
    -DSQLITECPP_BUILD_TESTS=ON \
    -DSQLITECPP_BUILD_EXAMPLES=OFF \
    ..
popd
%ninja_build -C %{_target_platform}

%check
pushd %{_target_platform}
    ctest --output-on-failure
popd

%install
%ninja_install -C %{_target_platform}

%files
%doc README.md CHANGELOG.md
%license LICENSE.txt
%{_libdir}/lib%{richname}.so.0*

%files devel
%{_includedir}/%{richname}
%{_libdir}/cmake/%{richname}
%{_libdir}/lib%{richname}.so

%changelog
* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 23 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 2.4.0-1
- Initial SPEC release.
