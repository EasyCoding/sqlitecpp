%global debug_package %{nil}
%global richname SQLiteCpp

Name: sqlitecpp
Version: 2.4.0
Release: 1%{?dist}

License: MIT
Summary: A smart and easy to use C++ SQLite3 wrapper
URL: https://github.com/SRombauts/%{richname}
Source0: %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

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
sed -e 's@DESTINATION lib@DESTINATION %{_lib}@g' -e 's@lib/@%{_lib}/@g' -i CMakeLists.txt
echo "set_property(TARGET SQLiteCpp PROPERTY SOVERSION 0)" >> CMakeLists.txt

%build
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    ..
popd
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}

%files
%{_libdir}/lib%{richname}.so.0*

%files devel
%doc README.md CHANGELOG.md
%license LICENSE.txt
%{_includedir}/%{richname}
%{_libdir}/cmake/%{richname}
%{_libdir}/lib%{richname}.so

%changelog
* Sat Nov 23 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 2.4.0-1
- Initial SPEC release.
