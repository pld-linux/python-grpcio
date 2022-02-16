# TODO:
# - system address_sorting and upb?
#
# Conditional build:
%bcond_without	apidocs		# (Python) API docs build
#
Summary:	HTTP/2 based RPC framework
Summary(pl.UTF-8):	Szkielet RPC oparty na HTTP/2
Name:		python-grpcio
Version:	1.39.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://github.com/grpc/grpc/releases
Source0:	https://github.com/grpc/grpc/archive/v%{version}/grpc-%{version}.tar.gz
# Source0-md5:	eafdc98790db2c85a5e5e79231ad875c
Patch0:		grpc-system-absl.patch
Patch1:		grpc-sphinx.patch
Patch2:		grpc-x32.patch
Patch3:		grpc-libdir.patch
Patch4:		grpc-system-openssl.patch
URL:		https://grpc.io/
BuildRequires:	abseil-cpp-devel
BuildRequires:	c-ares-devel >= 1.13.0
BuildRequires:	cmake >= 3.5.1
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	openssl-devel
BuildRequires:	protobuf-devel >= 3.12
BuildRequires:	python-Cython >= 0.23
BuildRequires:	python-modules >= 1:2.7
# with re2Config for cmake
BuildRequires:	re2-devel >= 20200801
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	python-Sphinx >= 1.8.1
BuildRequires:	python-six >= 1.10
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gRPC is a modern, open source, high-performance remote procedure call
(RPC) framework that can run anywhere. gRPC enables client and server
applications to communicate transparently, and simplifies the building
of connected systems.

%description -l pl.UTF-8
gRPC to nowoczesny, mający otwarty źródła, wydajny szkielet zdalnych
wywołań procedur (RPC - Remote Procedure Call). Pozwala na
przezroczystą komunikację klienta i serwera, upraszcza tworzenie
systemów połączonych.

%package apidocs
Summary:	API documentation for Python gRPC library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Pythona gRPC
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python gRPC library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Pythona gRPC.

%prep
%setup -q -n grpc-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
export GRPC_PYTHON_BUILD_SYSTEM_ABSL=1
export GRPC_PYTHON_BUILD_SYSTEM_CARES=1
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
export GRPC_PYTHON_BUILD_SYSTEM_RE2=1
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1

%if %{with apidocs}
export GRPC_PYTHON_ENABLE_DOCUMENTATION_BUILD=1
%endif
%py_build

%if %{with apidocs}
sphinx-build-2 -b html doc/python/sphinx doc/python/sphinx/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

export GRPC_PYTHON_BUILD_SYSTEM_ABSL=1
export GRPC_PYTHON_BUILD_SYSTEM_CARES=1
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
export GRPC_PYTHON_BUILD_SYSTEM_RE2=1
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1

%py_install

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dir %{py_sitedir}/grpc
%{py_sitedir}/grpc/*.py[co]
%dir %{py_sitedir}/grpc/_cython
%attr(755,root,root) %{py_sitedir}/grpc/_cython/cygrpc.so
%{py_sitedir}/grpc/_cython/__init__.py[co]
%{py_sitedir}/grpc/_cython/_credentials
%{py_sitedir}/grpc/_cython/_cygrpc
%{py_sitedir}/grpc/aio
%{py_sitedir}/grpc/beta
%{py_sitedir}/grpc/experimental
%{py_sitedir}/grpc/framework
%{py_sitedir}/grpcio-%{version}-py*.egg-info

%if %{with apidocs}
%files -n python-grpcio-apidocs
%defattr(644,root,root,755)
%doc doc/python/sphinx/_build/html/{_static,*.html,*.js}
%endif
