Name:           gd
Version:        2.2.5
Release:        7
Summary:        A graphics library for quick creation of PNG or JPEG images
License:        MIT
URL:            http://libgd.github.io/
Source0:        https://github.com/libgd/libgd/releases/download/gd-%{version}/libgd-%{version}.tar.xz

#PATCH-FIX-https://github.com/pisilinux/main/tree/master/multimedia/misc/gd/files
Patch0001:      gd-2.1.0-multilib.patch
#PATCH-CVE-2018-5711 - https://github.com/libgd/libgd/commit/a11f47475e6443b7f32d21f2271f28f417e2ac04
Patch0002:      gd-2.2.5-upstream.patch
#PATCH-FIX-OPENEULER
Patch6000:      CVE-2019-6977.patch
Patch6001:      CVE-2019-6978.patch
Patch6002:      CVE-2018-1000222.patch
Patch6003:      CVE-2019-11038.patch

BuildRequires:  freetype-devel fontconfig-devel gettext-devel libjpeg-devel libpng-devel libtiff-devel libwebp-devel gdb
BuildRequires:  libX11-devel libXpm-devel zlib-devel pkgconfig libtool perl-interpreter perl-generators liberation-sans-fonts

Provides:       %{name}-progs
Obsoletes:      %{name}-progs

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

%description    devel
The gd-devel package contains the development libraries and header files for gd, a graphics
library for creating PNG and JPEG graphics.The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images.

%prep
%autosetup -n libgd-%{version} -p1

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


%ifarch aarch64
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
export XFAIL_TESTS
make check

grep %{version} $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gdlib.pc

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_bindir}/*
%exclude %{_bindir}/gdlib-config

%files devel
%{_bindir}/gdlib-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gdlib.pc
%exclude %{_libdir}/libgd.la
%exclude %{_libdir}/libgd.a

%changelog
* Tue Aug 18 2020 smileknife<jackshan2010@aliyun.com> - 2.2.5-7
- update release for rebuilding

* Fri Mar 20 2020 songnannan <songnannan2@huawei.com> - 2.2.5-6
- add gdb in buildrequires

* Wed Sep 25 2019 wangli<wangli221@huawei.com>  2.2.5-5
- Type:cves
- ID:CVE-2019-11038
- SUG:NA
- DESC:fix cves

* Wed Sep 11 2019 openEuler jimmy<dukaitian@huawei.com> - 2.2.5-4
- Package init jimmy
