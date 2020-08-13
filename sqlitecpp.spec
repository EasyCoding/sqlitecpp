%undefine __cmake_in_source_build
%global richname SQLiteCpp

Name: sqlitecpp
Version: 3.1.0
Release: 1%{?dist}

License: MIT
Summary: Smart and easy to use C++ SQLite3 wrapper
URL: https://github.com/SRombauts/%{richname}
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

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

# Fixing W: wrong-file-end-of-line-encoding...
sed -e "s,\r,," -i README.md

# Removing bundled libraries...
rm -rf {sqlite3,googletest}

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DSQLITECPP_INTERNAL_SQLITE=OFF \
    -DSQLITECPP_BUILD_TESTS=ON \
    -DSQLITECPP_BUILD_EXAMPLES=OFF
%cmake_build

%check
%ctest

%install
%cmake_install

%files
%doc README.md CHANGELOG.md
%license LICENSE.txt
%{_libdir}/lib%{richname}.so.0*

%files devel
%{_includedir}/%{richname}
%{_libdir}/cmake/%{richname}
%{_libdir}/lib%{richname}.so

%changelog
* Thu Aug 13 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 3.1.0-1
- Updated to version 3.1.0.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 3.0.0-1
- Updated to version 3.0.0.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 23 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 2.4.0-1
- Initial SPEC release.
