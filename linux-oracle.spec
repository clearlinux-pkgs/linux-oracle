#
# note to self: Linus releases need to be named 5.x.0 not 5.x or various
# things break
# 
#

Name:           linux-oracle
Version:        5.6.6
Release:        142
License:        GPL-2.0
Summary:        The Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.6.6.tar.xz
Source1:        config
Source2:        cmdline

%define ktarget  oracle
%define kversion %{version}-%{release}.%{ktarget}

BuildRequires:  buildreq-kernel
BuildRequires:  dhcp
BuildRequires:  dracut
BuildRequires:  iproute2
BuildRequires:  iputils
BuildRequires:  open-iscsi
BuildRequires:  systemd
BuildRequires:  util-linux

Requires: systemd-bin
Requires: linux-oracle-license = %{version}-%{release}

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

#cve.start cve patches from 0001 to 050
#cve.end

#mainline: Mainline patches, upstream backport and fixes from 0051 to 0099
#mainline.end

#Serie.clr 01XX: Clear Linux patches
Patch0101: 0101-i8042-decrease-debug-message-level-to-info.patch
Patch0102: 0102-Increase-the-ext4-default-commit-age.patch
Patch0103: 0103-silence-rapl.patch
Patch0104: 0104-pci-pme-wakeups.patch
Patch0105: 0105-ksm-wakeups.patch
Patch0106: 0106-intel_idle-tweak-cpuidle-cstates.patch
Patch0107: 0107-bootstats-add-printk-s-to-measure-boot-time-in-more-.patch
Patch0108: 0108-smpboot-reuse-timer-calibration.patch
Patch0109: 0109-raid6-add-Kconfig-option-to-skip-raid6-benchmarking.patch
Patch0110: 0110-Initialize-ata-before-graphics.patch
Patch0111: 0111-give-rdrand-some-credit.patch
Patch0112: 0112-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch
Patch0113: 0113-kernel-time-reduce-ntp-wakeups.patch
Patch0114: 0114-init-wait-for-partition-and-retry-scan.patch
Patch0115: 0115-print-fsync-count-for-bootchart.patch
Patch0116: 0116-Add-boot-option-to-allow-unsigned-modules.patch
Patch0117: 0117-Enable-stateless-firmware-loading.patch
Patch0118: 0118-Migrate-some-systemd-defaults-to-the-kernel-defaults.patch
Patch0119: 0119-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch
Patch0120: 0120-add-scheduler-turbo3-patch.patch
Patch0121: 0121-use-lfence-instead-of-rep-and-nop.patch
Patch0122: 0122-do-accept-in-LIFO-order-for-cache-efficiency.patch
Patch0123: 0123-zero-extra-registers.patch
Patch0124: 0124-locking-rwsem-spin-faster.patch
Patch0125: 0125-ata-libahci-ignore-staggered-spin-up.patch
Patch0126: 0126-print-CPU-that-faults.patch
Patch0127: 0127-x86-microcode-Force-update-a-uCode-even-if-the-rev-i.patch
Patch0128: 0128-x86-microcode-echo-2-reload-to-force-load-ucode.patch
Patch0129: 0129-fix-bug-in-ucode-force-reload-revision-check.patch
Patch0130: 0130-nvme-workaround.patch
Patch0131: 0131-Don-t-report-an-error-if-PowerClamp-run-on-other-CPU.patch
#Serie.end

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel oracle extra files
Group:          kernel
Requires:       linux-oracle-license = %{version}-%{release}

%description extra
Linux kernel extra files

%package license
Summary: license components for the linux package.
Group: Default

%description license
license components for the linux package.

%prep
%setup -q -n linux-5.6.6

#cve.patch.start cve patches
#cve.patch.end

#mainline.patch.start Mainline patches, upstream backport and fixes
#mainline.patch.end

#Serie.patch.start Clear Linux patches
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1
%patch0124 -p1
%patch0125 -p1
%patch0126 -p1
%patch0127 -p1
%patch0128 -p1
%patch0129 -p1
%patch0130 -p1
%patch0131 -p1
#Serie.patch.end

cp %{SOURCE1} .

%build
BuildKernel() {

    Target=$1
    Arch=x86_64
    ExtraVer="-%{release}.${Target}"

    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = ${ExtraVer}/" Makefile

    make O=${Target} -s mrproper
    cp config ${Target}/.config

    make O=${Target} -s ARCH=${Arch} olddefconfig
    make O=${Target} -s ARCH=${Arch} CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} %{?sparse_mflags}
}

BuildKernel %{ktarget}

touch abifiles.list

%install

InstallKernel() {

    Target=$1
    Kversion=$2
    Arch=x86_64
    KernelDir=%{buildroot}/usr/lib/kernel

    mkdir   -p ${KernelDir}
    install -m 644 ${Target}/.config    ${KernelDir}/config-${Kversion}
    install -m 644 ${Target}/System.map ${KernelDir}/System.map-${Kversion}
    install -m 644 ${Target}/vmlinux    ${KernelDir}/vmlinux-${Kversion}
    install -m 644 %{SOURCE2}           ${KernelDir}/cmdline-${Kversion}
    cp  ${Target}/arch/x86/boot/bzImage ${KernelDir}/org.clearlinux.${Target}.%{version}-%{release}
    chmod 755 ${KernelDir}/org.clearlinux.${Target}.%{version}-%{release}

    mkdir -p %{buildroot}/usr/lib/modules
    make O=${Target} -s ARCH=${Arch} INSTALL_MOD_PATH=%{buildroot}/usr modules_install

    rm -f %{buildroot}/usr/lib/modules/${Kversion}/build
    rm -f %{buildroot}/usr/lib/modules/${Kversion}/source

    # Kernel default target link
    ln -s org.clearlinux.${Target}.%{version}-%{release} %{buildroot}/usr/lib/kernel/default-${Target}
}

# cpio file
createInitrd() {

    Target=$1
    Kversion=$2

    # hack since dhclient is not where dracut expects it to be
    export DRACUT_PATH=/usr/libexec/:$PATH
    dracut --kmoddir %{buildroot}/usr/lib/modules/%{version}-%{release}.${Target} \
           --kver %{version}-%{release}.${Target} \
           -m "base bash dracut-systemd fs-lib iscsi network rootfs-block shutdown systemd systemd-initrd udev-rules usrmount" \
           --include /usr/libexec/dhclient /usr/bin/dhclient \
           tmp-initrd
    # hack since dracut misses some key pieces to actually be able to mount the iscsi rootfs
    mkdir t
    cd t
    lsinitrd --unpack ../tmp-initrd
    cp /usr/lib64/libisns.so.* usr/lib64/
    cp /usr/bin/iscsid usr/bin/
    cp /usr/bin/iscsiadm usr/bin/
    find . | cpio -o -H newc \
      | gzip > %{buildroot}/usr/lib/kernel/initrd-org.clearlinux.${Target}.%{version}-%{release}
    cd ..
}

InstallKernel %{ktarget} %{kversion}

createInitrd %{ktarget} %{kversion}

rm -rf %{buildroot}/usr/lib/firmware

mkdir -p %{buildroot}/usr/share/package-licenses/linux-oracle
cp COPYING %{buildroot}/usr/share/package-licenses/linux-oracle/COPYING
cp -a LICENSES/* %{buildroot}/usr/share/package-licenses/linux-oracle

%files
%dir /usr/lib/kernel
%dir /usr/lib/modules/%{kversion}
/usr/lib/kernel/config-%{kversion}
/usr/lib/kernel/cmdline-%{kversion}
/usr/lib/kernel/initrd-org.clearlinux.%{ktarget}.%{version}-%{release}
/usr/lib/kernel/org.clearlinux.%{ktarget}.%{version}-%{release}
/usr/lib/kernel/default-%{ktarget}
/usr/lib/modules/%{kversion}/kernel
/usr/lib/modules/%{kversion}/modules.*

%files extra
%dir /usr/lib/kernel
/usr/lib/kernel/System.map-%{kversion}
/usr/lib/kernel/vmlinux-%{kversion}

%files license
%defattr(0644,root,root,0755)
/usr/share/package-licenses/linux-oracle
