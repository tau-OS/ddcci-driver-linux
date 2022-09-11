# (un)define the next line to either build for the newest or all current kernels. You will most likely want akmod
# define buildforkernels newest
# define buildforkernels current
%define buildforkernels akmod
%global debug_package %{nil}

# name should have a -kmod suffix
Name:           example-kmod

Version:        1
Release:        1%{?dist}.1
Summary:        Example kernel modules

Group:          System Environment/Kernel

License:        MIT
URL:            https://example.com
Source0:        https://example.com/example.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{_bindir}/kmodtool


# Verify that the package build for all architectures.
# In most time you should remove the Exclusive/ExcludeArch directives
# and fix the code (if needed).
# ExclusiveArch:  x86_64
# ExcludeArch: i686 x86_64 ppc64 ppc64le armv7hl aarch64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
BuildRequires:  %{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The example kernel modules.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

# apply patches and do other stuff here
# pushd example
# #patch0 -p1 -b .suffix
# popd
for kernel_version in %{?kernel_versions} ; do
    # The "example" name here is the resulting folder after the extracting Source0, same for the pushd above
    cp -a example _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}
    make V=1 %{?_smp_mflags} -C "${kernel_version##*___}" M=`pwd` SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*} modules
    popd
done

%install
rm -rf ${RPM_BUILD_ROOT}

for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}
    mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
    make V=1 -C "${kernel_version##*___}" M=`pwd` INSTALL_MOD_PATH=${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix} modules_install
    popd
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT
