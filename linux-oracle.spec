#
# note to self: Linus releases need to be named 4.x.0 not 4.x or various
# things break
#

Name:           linux-oracle
Version:        5.0.10
Release:        38
License:        GPL-2.0
Summary:        The Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.0.10.tar.xz
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

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

#    000X: cve, bugfixes patches

#    00XY: Mainline patches, upstream backports

#          BBR perf fix backport
Patch0050: 0050-tcp_bbr-refactor-bbr_target_cwnd-for-general-infligh.patch
Patch0051: 0051-tcp_bbr-adapt-cwnd-based-on-ack-aggregation-estimati.patch

# Serie    01XX- Clear Linux patches
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
Patch0111: 0111-reduce-e1000e-boot-time-by-tightening-sleep-ranges.patch
Patch0112: 0112-give-rdrand-some-credit.patch
Patch0113: 0113-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch
Patch0114: 0114-tweak-perfbias.patch
Patch0115: 0115-e1000e-increase-pause-and-refresh-time.patch
Patch0116: 0116-kernel-time-reduce-ntp-wakeups.patch
Patch0117: 0117-init-wait-for-partition-and-retry-scan.patch
Patch0118: 0118-print-fsync-count-for-bootchart.patch
Patch0119: 0119-Add-boot-option-to-allow-unsigned-modules.patch
Patch0120: 0120-Enable-stateless-firmware-loading.patch
Patch0121: 0121-Migrate-some-systemd-defaults-to-the-kernel-defaults.patch
Patch0122: 0122-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch
Patch0123: 0123-add-scheduler-turbo3-patch.patch
Patch0124: 0124-use-lfence-instead-of-rep-and-nop.patch
Patch0125: 0125-do-accept-in-LIFO-order-for-cache-efficiency.patch
Patch0126: 0126-zero-extra-registers.patch
Patch0127: 0127-locking-rwsem-spin-faster.patch
#Serie.clr.end

#Serie1.name WireGuard
#Serie1.git  https://git.zx2c4.com/WireGuard
#Serie1.cmt  91b0a211861d487382a534572844ff29839064f1
#Serie1.tag  0.0.20190406
Patch1001: 1001-WireGuard-fast-modern-secure-kernel-VPN-tunnel.patch
#Serie1.end

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel

%description extra
Linux kernel extra files

%prep
%setup -q -n linux-5.0.10

#     000X  cve, bugfixes patches

#     00XY  Mainline patches, upstream backports

#           BBR perf fix bacport
%patch0050 -p1
%patch0051 -p1

#     01XX  Clear Linux patches
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
#%patch0126 -p1
%patch0127 -p1

#Serie1.patch.start
%patch1001 -p1
#Serie1.patch.end

cp %{SOURCE1} .

cp -a /usr/lib/firmware/i915 firmware/
cp -a /usr/lib/firmware/intel-ucode firmware/

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

# cpio file for i8042 libps2 atkbd
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
}

InstallKernel %{ktarget} %{kversion}

createInitrd %{ktarget} %{kversion}

rm -rf %{buildroot}/usr/lib/firmware

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
