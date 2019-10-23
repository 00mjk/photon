Summary:        Management tools and libraries relating to cryptography
Name:           nxtgn-openssl
Version:        1.1.1d
Release:        1%{?dist}
License:        OpenSSL
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.openssl.org/source/openssl-%{version}.tar.gz
%define sha1    openssl=056057782325134b76d1931c48f2c7e6595d7ef4
Source1:        nxtgn-rehash_ca_certificates.sh
Patch1:         nxtgn-c_rehash.patch
%if %{with_check}
BuildRequires: zlib-devel
%endif
Requires:       bash glibc libgcc

%description
The OpenSSL package contains management tools and libraries relating
to cryptography. These are useful for providing cryptography
functions to other packages, such as OpenSSH, email applications and
web browsers (for accessing HTTPS sites).

%package devel
Summary: Development Libraries for nxtgn-openssl
Group: Development/Libraries
Requires: nxtgn-openssl = %{version}-%{release}
Obsoletes:  openssl-devel
%description devel
Header files for doing development with openssl.

%package perl
Summary: nxtgn openssl perl scripts
Group: Applications/Internet
Requires: perl
Requires: nxtgn-openssl = %{version}-%{release}
%description perl
Perl scripts that convert certificates and keys to various formats.

%package c_rehash
Summary: nxtgn openssl perl scripts
Group: Applications/Internet
Requires: perl
Requires: perl-DBI
Requires: perl-DBIx-Simple
Requires: perl-DBD-SQLite
Requires: nxtgn-openssl = %{version}-%{release}
%description c_rehash
Perl scripts that convert certificates and keys to various formats.

%prep
%setup -q -n openssl-%{version}
%patch1 -p1

%build
export CFLAGS="%{optflags}"
./config \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --openssldir=%{_sysconfdir}/nxtgn-openssl \
    --shared \
# does not support -j yet
make
%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=nxtgn-openssl install
install -p -m 755 -D %{SOURCE1} %{buildroot}%{_bindir}/

mv %{buildroot}/%{_includedir}/openssl %{buildroot}/%{_includedir}/nxtgn-openssl
mv %{buildroot}/%{_bindir}/openssl %{buildroot}/%{_bindir}/nxtgn-openssl
mv %{buildroot}/%{_bindir}/c_rehash %{buildroot}/%{_bindir}/nxtgn-c_rehash

ln -sf libssl.so.1.1* %{buildroot}%{_libdir}/libssl.so.1.1.0
ln -sf libcrypto.so.1.1* %{buildroot}%{_libdir}/libcrypto.so.1.1.0

%check
make tests

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/nxtgn-openssl/certs
%{_sysconfdir}/nxtgn-openssl/ct_log_list.cnf
%{_sysconfdir}/nxtgn-openssl/ct_log_list.cnf.dist
%{_sysconfdir}/nxtgn-openssl/openssl.cnf.dist
%{_sysconfdir}/nxtgn-openssl/openssl.cnf
%{_sysconfdir}/nxtgn-openssl/private
%{_bindir}/nxtgn-openssl
%{_libdir}/libssl.so.*
%{_libdir}/libcrypto.so.*
%{_libdir}/engines*/*
%exclude %{_mandir}/man1/*
%exclude %{_mandir}/man5/*
%exclude %{_mandir}/man7/*
%exclude %{_docdir}/*

%files devel
%{_includedir}/nxtgn-openssl/
%exclude %{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libssl.a
%{_libdir}/libcrypto.a
%{_libdir}/libssl.so
%{_libdir}/libcrypto.so

%files perl
/%{_sysconfdir}/nxtgn-openssl/misc/tsget
/%{_sysconfdir}/nxtgn-openssl/misc/tsget.pl
/%{_sysconfdir}/nxtgn-openssl/misc/CA.pl

%files c_rehash
/%{_bindir}/nxtgn-c_rehash
/%{_bindir}/nxtgn-rehash_ca_certificates.sh

%changelog
*   Tue Sep 03 2019 Tapas Kundu <tkundu@vmware.com> 1.1.1d-1
-   Package OpenSSL 1.1.1d.