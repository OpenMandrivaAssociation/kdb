%define major 4
%define libname %mklibname KDb3 %{major}
%define devname %mklibname KDb3 -d
%define olibname %mklibname KDb3 3

Name:		kdb
Version:	3.2.0
Release:	5
Source0:	http://download.kde.org/stable/kdb/src/%{name}-%{version}.tar.xz
Patch0:		kdb-3.2.0-postgresql-12.patch
Patch1:		kdb-3.2.0-dont-reference-nonexistant-pkgconfig-files.patch
Summary:	Database connectivity and creation framework
URL:		http://community.kde.org/KDb/About_KDb
License:	LGPLv2+
Group:		System/Libraries
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5Xml)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5Network)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(mariadb)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5CoreAddons)
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	qt5-assistant
Requires:	%{libname} = %{EVRD}

%description
KDb is a database connectivity and creation framework for various database
vendors.

KDb consists of a general-purpose C++/Qt-only library and a set of plugins.
Because there is no dependency on Kexi, Calligra or even on KDE libraries,
KDb can be developed for a wider audience.
Kexi since the version 3 uses it too, thus deprecating KexiDB.

Unlike QtSQL, KDb 'knows' how to create database and new tables. It has a
Qt/C++ API for that. There is no need to pass SQL at all but you can pass
it if you wish (it will silently parse your statements before contacting
the database).

KDb is developed as a next generation database handling layer for Kexi
and similar complex apps.


%package -n %{libname}
Summary: A database connectivity and creation framework for various databases
Group: System/Libraries
Requires: %{name} = %{EVRD}
Requires: %{name}-plugin = %{EVRD}
Obsoletes: %{olibname}

%description -n %{libname}
A database connectivity and creation framework for various databases

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%{name} is a database connectivity and creation framework for various databases.

%package mysql
Summary: MariaDB/MySQL support plugin for KDb
Group: System/Libraries
Requires: %{libname} = %{EVRD}
Provides: %{name}-plugin = %{EVRD}

%description mysql
MariaDB/MySQL support plugin for KDb

%package postgresql
Summary: PostgreSQL support plugin for KDb
Group: System/Libraries
Requires: %{libname} = %{EVRD}
Provides: %{name}-plugin = %{EVRD}

%description postgresql
PostgreSQL support plugin for KDb

%package sqlite
Summary: SQLite support plugin for KDb
Group: System/Libraries
Requires: %{libname} = %{EVRD}
Provides: %{name}-plugin = %{EVRD}

%description sqlite
SQLite support plugin for KDb

%prep
%autosetup -p1
export PATH=%{_libdir}/qt5/bin:$PATH
%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build
%find_lang kdb_mysqldriver --with-qt
%find_lang kdb_postgresqldriver --with-qt
%find_lang kdb --with-qt
%find_lang kdb_sqlitedriver --with-qt
#find_lang kdb_sybasedriver --with-qt
#find_lang kdb_xbasedriver --with-qt

%files -f kdb.lang
%{_bindir}/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files mysql -f kdb_mysqldriver.lang
%{_libdir}/qt5/plugins/kdb3/kdb_mysqldriver.so

%files postgresql -f kdb_postgresqldriver.lang
%{_libdir}/qt5/plugins/kdb3/kdb_postgresqldriver.so

%files sqlite -f kdb_sqlitedriver.lang
%{_libdir}/qt5/plugins/kdb3/kdb_sqlitedriver.so
%{_libdir}/qt5/plugins/kdb3/sqlite3/kdb_sqlite_icu.so

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/KDb3
%{_libdir}/qt5/mkspecs/modules/qt_KDb3.pri
%doc %{_docdir}/qt5/*
