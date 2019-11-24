%global richname SQLiteCpp

Name: sqlitecpp
Version: 2.4.0
Release: 1%{?dist}

License: MIT
Summary: Smart and easy to use C++ SQLite3 wrapper
URL: https://github.com/SRombauts/%{richname}
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: sqlite-devel
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
%autosetup -n %{richname}-%{version}
mkdir -p %{_target_platform}

# Fixing W: wrong-file-end-of-line-encoding...
sed -e "s,\r,," -i README.md

# Patching CMakeLists...
sed -e 's@DESTINATION lib@DESTINATION %{_lib}@g' -e 's@lib/@%{_lib}/@g' -i CMakeLists.txt
echo "set_property(TARGET SQLiteCpp PROPERTY SOVERSION 0)" >> CMakeLists.txt

# Removing bundled libraries...
rm -rf sqlite3
rm -rf googletest

%build
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DSQLITECPP_INTERNAL_SQLITE=OFF \
    -DSQLITECPP_BUILD_TESTS=OFF \
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
* Sat Nov 23 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 2.4.0-1
- Initial SPEC release.
