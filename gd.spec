Name:           gd
Version:        2.3.3
Release:        3
Summary:        A graphics library for quick creation of PNG or JPEG images
License:        MIT
URL:            http://libgd.github.io/
Source0:        https://github.com/libgd/libgd/releases/download/gd-%{version}/libgd-%{version}.tar.xz

# Missing, temporary workaround, fixed upstream for next version
Source1:        https://raw.githubusercontent.com/libgd/libgd/gd-%{version}/config/getlib.sh
Patch0:		libgd-flip.patch

BuildRequires:  freetype-devel fontconfig-devel gettext-devel libjpeg-devel libpng-devel libtiff-devel libwebp-devel
BuildRequires:  libX11-devel libXpm-devel zlib-devel pkgconfig libtool perl-interpreter perl-generators liberation-sans-fonts

%description
The gd graphics library allows your code to quickly draw images complete with lines, arcs, text,
multiple colors, cut and paste from other images, and flood fills, and to write out the result as a PNG or
JPEG file. The most common applications of GD involve website development,
although it can be used with any standalone application!

%package        devel
Summary:        The development libraries and header files for gd
Requires:       %{name}%{?_isa} = %{version}-%{release} freetype-devel%{?_isa} fontconfig-devel%{?_isa} libjpeg-devel%{?_isa}
Requires:       libpng-devel%{?_isa} libtiff-devel%{?_isa} libwebp-devel%{?_isa} libX11-devel%{?_isa}
Requires:       libXpm-devel%{?_isa} zlib-devel%{?_isa}

%package progs
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Utility programs that use libgd

%description progs
The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images.

%description    devel
The gd-devel package contains the development libraries and header files for gd, a graphics
library for creating PNG and JPEG graphics.The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images.

%prep
%autosetup -n libgd-%{version} -p1
install -m 0755 %{SOURCE1} config/

: $(perl config/getver.pl)

: regenerate autotool stuff
if [ -f configure ]; then
   libtoolize --copy --force
   autoreconf -vif
else
   ./bootstrap.sh
fi

%build
CFLAGS="$RPM_OPT_FLAGS -DDEFAULT_FONTPATH='\"\
/usr/share/fonts/bitstream-vera:\
/usr/share/fonts/dejavu:\
/usr/share/fonts/default/Type1:\
/usr/share/X11/fonts/Type1:\
/usr/share/fonts/liberation\"'"

%ifarch %{ix86}
# see https://github.com/libgd/libgd/issues/242
export CFLAGS="$CFLAGS -msse -mfpmath=sse"
%endif

%ifarch aarch64 ppc64 ppc64le s390 s390x loongarch64
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1359680
export CFLAGS="$CFLAGS -ffp-contract=off"
%endif

%configure \
    --with-tiff=%{_prefix} \
    --disable-rpath
%make_build

%install
%make_install

%check
export TMPDIR=/tmp
make check

grep %{version} $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gdlib.pc

%ldconfig_scriptlets

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/*.so.*
%exclude %{_bindir}/gdlib-config

%files progs
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gdlib.pc
%exclude %{_libdir}/libgd.la
%exclude %{_libdir}/libgd.a

%changelog
* Mon Feb 13 2023 zhangpan <zhangpan103@h-partners.com> - 2.3.3-3
- fix build error for loongarch64

* Sun Nov 13 2022 Funda Wang <fundawang@yeah.net> - 2.3.3-2
- Add patch from fedora to fix build with PHP

* Sat Oct 29 2022 zhouwenpei <zhouwenpei1@h-partners.com> - 2.3.3-1
- update to 2.3.3

* Fri Apr 08 2022 dongyuzhen <dongyuzhen@h-partners.com> - 2.3.2-2
- fix CVE-2021-40145

* Sat Nov 20 2021 hanhui<hanhui15@huawei.com> - 2.3.2-1
- DESC:update to 2.3.2

* Thu Sep 23 2021 liuyumeng<liuyumeng5@huawei.com> - 2.3.0-4
- Type:CVE
- CVE:CVE-2021-40812
- SUG:NA
- DESC:fix CVE-2021-40812

* Sat Aug 14 2021 zhanzhimin<zhanzhimin@huawei.com> - 2.3.0-3
- Type:CVE
- ID:CVE-2021-38115
- SUG:NA
- DESC:fix CVE-2021-38115

* Tue Jul 20 2021 zhanzhimin<zhanzhimin@huawei.com> - 2.3.0-2
- delete gdb buildrequires

* Thu Jul 23 2020 zhangqiumiao<zhangqiumiao1@huawei.com> - 2.3.0-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:upgrade to version 2.3.0

* Fri Mar 20 2020 songnannan <songnannan2@huawei.com> - 2.2.5-6
- add gdb in buildrequires

* Wed Sep 25 2019 wangli<wangli221@huawei.com> - 2.2.5-5
- Type:cves
- ID:CVE-2019-11038
- SUG:NA
- DESC:fix cves

* Wed Sep 11 2019 openEuler jimmy<dukaitian@huawei.com> - 2.2.5-4
- Package init jimmy
