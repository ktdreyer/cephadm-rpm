# Upstream ceph commit upon which this package is based:
# patches_base=74275226ac79999bfd40e683dc9a1309e76033bf

Name:    cephadm
Epoch:   2
Version: 16.1.0
Release: 100%{?dist}
Summary: Utility to bootstrap Ceph clusters
License: LGPL-2.1
URL:     https://ceph.io
Source0: https://github.com/ceph/ceph/raw/74275226ac79999bfd40e683dc9a1309e76033bf/src/cephadm/cephadm
Source1: COPYING-LGPL2.1

BuildArch: noarch

Requires:       lvm2
Requires:       python3
Recommends:     podman
%description
Utility to bootstrap a Ceph cluster and manage Ceph daemons deployed
with systemd and podman.

%prep
cp %{SOURCE0} .
cp %{SOURCE1} .

%build

%install
mkdir -p %{buildroot}%{_sbindir}
install -m 0755 cephadm %{buildroot}%{_sbindir}/cephadm
mkdir -p %{buildroot}%{_sharedstatedir}/cephadm
chmod 0700 %{buildroot}%{_sharedstatedir}/cephadm
mkdir -p %{buildroot}%{_sharedstatedir}/cephadm/.ssh
chmod 0700 %{buildroot}%{_sharedstatedir}/cephadm/.ssh
touch %{buildroot}%{_sharedstatedir}/cephadm/.ssh/authorized_keys
chmod 0600 %{buildroot}%{_sharedstatedir}/cephadm/.ssh/authorized_keys

%pre
getent group cephadm >/dev/null || groupadd -r cephadm
getent passwd cephadm >/dev/null || useradd -r -g cephadm -s /bin/bash -c "cephadm user for mgr/cephadm" -d %{_sharedstatedir}/cephadm cephadm
exit 0

%postun
userdel -r cephadm || true
exit 0

%files
%license COPYING-LGPL2.1
%{_sbindir}/cephadm
%attr(0700,cephadm,cephadm) %dir %{_sharedstatedir}/cephadm
%attr(0700,cephadm,cephadm) %dir %{_sharedstatedir}/cephadm/.ssh
%attr(0600,cephadm,cephadm) %{_sharedstatedir}/cephadm/.ssh/authorized_keys

%changelog
* Wed Feb 10 2021 Ken Dreyer <kdreyer@redhat.com> - 16.1.0-100
- initial package

