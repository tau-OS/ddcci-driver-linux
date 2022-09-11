# rpm-kmod-template

This is a simple base to build -kmod packages for tauOS and other RPM based systems, based on the [rpmfusion kmods example](https://rpmfusion.org/Packaging/KernelModules/Kmods2). For modules that are built using standard [kbuild](https://www.kernel.org/doc/Documentation/kbuild/modules.txt) (hopefully most modules) it should just work:tm: after basic customization of the spec files.

## Usage

For development, make sure that you have the rpmfusion repos enabled. The rest is just filling the RPM spec with the relevant values.