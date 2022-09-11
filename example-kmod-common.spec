Name:           example-kmod-common

Version:        1
Release:        1%{?dist}.1
Summary:        Common files for the example kernel modules

Group:          System Environment/Kernel

License:        MIT
URL:            https://example.com
Source0:        https://example.com/example.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%description
These are the common files: LICENSE, config, etc... for the example kernel modules.

%prep
%setup -q -c -T -a 0

%files

%clean
rm -rf $RPM_BUILD_ROOT
