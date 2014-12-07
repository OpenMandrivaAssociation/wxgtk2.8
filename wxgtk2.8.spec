%define		oname		wxGTK
%define		majorminor	2.8
%define		major		%{majorminor}

%define		libname		%mklibname wxgtk %{major}
%define		libnamedev	%mklibname -d wxgtk %{major}
%define		libgl		%mklibname wxgtkgl %{major}

%define		libnameu	%mklibname wxgtku %{major}
%define		libnameudev	%mklibname -d wxgtku %{major}
%define		libglu		%mklibname wxgtkglu %{major}

Summary:	GTK+ port of the wxWidgets library
Name:		wxgtk%{majorminor}
Version:	2.8.12
Release:	19
License:	wxWidgets Library Licence
Group:		System/Libraries
URL:		http://www.wxwidgets.org/
Source0:	http://prdownloads.sourceforge.net/wxwindows/%{oname}-%{version}.tar.bz2
#gw security patch for bundled expat which we don't use:
Patch2:		wxGTK-2.8.10-CVE-2009-XXXX.diff
Patch3:		wxGTK-lX11_linkage_fix.diff
Patch8:		wxWidgets-2.7.0-multiarch-includes.patch
#gw security patch for bundled expat which we don't use:
Patch9:		wxGTK-2.8.8-CVE-2009-3560.diff
Patch10:	wxGTK-2.8.12-fix-user_data-casting.patch
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
Buildrequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	tiff-devel
Buildrequires:	bison, flex
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires:	pkgconfig(gconf-2.0)

%description
wxWidgets is a free C++ library for cross-platform GUI development.
With wxWidgets, you can create applications for different GUIs (GTK+,
Motif/LessTif, MS Windows, Mac) from the same source code.

%package -n	%{libnameu}
Group:		System/Libraries
Summary: 	Base shared library part of wxGTK - Unicode enabled
Requires:	%{name} = %{version}-%{release}
%rename		%{libname}

%description -n	%{libnameu}
wxWidgets is a free C++ library for cross-platform GUI development.
With wxWidgets, you can create applications for different GUIs (GTK+,
Motif/LessTif, MS Windows, Mac) from the same source code.

This package contains the library needed to run programs dynamically
linked with the unicode enabled version of %{name}.

%package -n	%{libnameudev}
Summary:	Header files and development documentation for wxGTK - unicode
Group:		Development/C++
Requires:	%{libnameu} = %{version}-%{release}
Requires:	%{libglu} = %{version}-%{release}
Provides:	libwxgtku-devel = %{version}-%{release}
Provides:	wxgtku-devel = %{version}-%{release}
Provides:	wxgtku%{majorminor}-devel = %{version}-%{release}
Provides:	libwxgtku%{majorminor}-devel = %{version}-%{release}
%rename		wxGTK-devel
%rename		%{libnamedev}

%description -n	%{libnameudev}
Header files for the unicode enabled version of wxGTK, the GTK+ port of
the wxWidgets library.

%package -n	%{libglu}
Summary:	GTK+ port of the wxWidgets library, OpenGl add-on - unicode
Group:		System/Libraries
%rename		wxGTK-gl
%rename		%{libgl}

%description -n	%{libglu}
OpenGl add-on library for the unicode enabled version of wxGTK, the
GTK+ port of the wxWidgets library.

%prep
%setup -q -n %{oname}-%{version}
%patch2 -p0 -b .CVE-2009-XXXX
%patch3 -p1
%patch8 -p1 -b .multiarch
%patch9 -p0 -b .CVE-2009-3560
%patch10 -p1 -b .cast~
sed -i -e 's/@LDFLAGS@//' wx-config.in

# fix plugin dir for 64-bit
sed -i -e 's|/lib|/%{_lib}|' src/unix/stdpaths.cpp

find samples demos -name .cvsignore -exec rm {} \;

%build
#gw 2.8.11 doesn't build otherwise:
%define _disable_ld_no_undefined 1
%define Werror_cflags %nil
# --disable-optimise prevents our $RPM_OPT_FLAGS being overridden
# (see OPTIMISE in configure).
# this code dereferences type-punned pointers like there's no tomorrow.
CFLAGS="%{optflags} -fno-strict-aliasing"
CXXFLAGS="%{optflags} -fno-strict-aliasing"

%configure2_5x --enable-unicode \
	--without-odbc \
	--with-opengl \
	--enable-gtk2 --with-gtk  \
	--without-debug_flag \
	--without-debug_info \
	--with-sdl \
	--with-libpng=sys \
	--with-libjpeg=sys \
	--with-libtiff=sys \
	--with-zlib=sys \
	--disable-optimise \
	--enable-calendar \
	--enable-wave \
	--enable-fraction \
	--enable-wxprintfv \
	--enable-xresources \
	--enable-controls \
	--enable-tabdialog \
	--enable-msgdlg \
	--enable-dirdlg \
	--enable-numberdlg \
	--enable-splash \
	--enable-textdlg \
	--enable-graphics_ctx \
	--enable-grid \
	--disable-catch_segvs \
	--enable-mediactrl \
	--enable-dataviewctrl

%make

%make -C locale allmo
%make -C contrib
#gw prepare samples
cd demos
make clean
%__rm -f makefile* demos.bkl
cd ../samples
make clean
%__rm -f makefile* samples.bkl
cd ..
find demos samples -name Makefile|xargs perl -pi -e 's^CXXC =.*^CXXC=\$(CXX) `wx-config --cflags`^'
find demos samples -name Makefile|xargs perl -pi -e 's^EXTRALIBS =.*^EXTRALIBS=^'
find demos samples -name Makefile|xargs perl -pi -e 's^SAMPLES_RPATH_FLAG =.*^SAMPLES_RPATH_FLAG=^'

%install
%__rm -rf %{buildroot}
%makeinstall
%find_lang wxstd
%find_lang wxmsw
cat wxmsw.lang >> wxstd.lang
%makeinstall -C contrib
mv %{buildroot}%{_bindir}/wxrc-%{majorminor} %{buildroot}%{_bindir}/wxrc-%{majorminor}-unicode
###
#gw fix broken symlink
rm -f %{buildroot}%{_bindir}/{wx-config,wxrc}
ln -sf %{_libdir}/wx/config/gtk2-unicode-release-%{majorminor} %{buildroot}%{_bindir}/wx-config-unicode

%multiarch_binaries %{buildroot}%{_libdir}/wx/config/gtk2-unicode-release-%{majorminor}

#gw this breaks /usr/bin/wx-config
mkdir %{buildroot}%{multiarch_bindir}
ln -s %{_libdir}/wx/config/%{multiarch_platform}/gtk2-unicode-release-%{majorminor} %{buildroot}%{multiarch_bindir}/wx-config-unicode
%multiarch_includes %{buildroot}%{_libdir}/wx/include/gtk2-unicode-release-%{majorminor}/wx/setup.h

%multiarch_includes %{buildroot}%{_includedir}/wx-%{majorminor}/wx/defs.h

#gw remove Mandriva linker flags
sed -i -e "s^-Wl,--as-needed^^g" %{buildroot}%{_libdir}/wx/config/%{multiarch_platform}/*

%post -n %{libnameudev}
update-alternatives --install %{_bindir}/wx-config wx-config %{_libdir}/wx/config/gtk2-unicode-release-%{majorminor} 15 --slave %{_bindir}/wxrc wxrc %{_bindir}/wxrc-%{majorminor}-unicode
%postun -n %{libnameudev}
if [ "$1" = "0" ]; then
  update-alternatives --remove wx-config %{_libdir}/wx/config/gtk2-unicode-release-%{majorminor} 
fi

%files -f wxstd.lang
%doc *.txt

%files -n %{libnameu}
%{_libdir}/libwx_gtk2u_adv-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_aui-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_core-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_html-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_richtext-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_media-%{majorminor}.so.*
%{_libdir}/libwx_baseu-%{majorminor}.so.*
%{_libdir}/libwx_baseu_net-%{majorminor}.so.*
%{_libdir}/libwx_baseu_xml-%{majorminor}.so.*
# contribs
%{_libdir}/libwx_gtk2u_fl-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_gizmos-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_gizmos_xrc-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_ogl-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_plot-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_qa-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_stc-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_svg-%{majorminor}.so.*
%{_libdir}/libwx_gtk2u_xrc-%{majorminor}.so.*

%files -n %{libnameudev}
%doc samples/
%doc docs/
%doc demos/
%{_bindir}/wx-config-unicode
%{_bindir}/wxrc-*unicode
%{multiarch_bindir}/wx-config-unicode
%{_includedir}/wx-%{majorminor}/
%dir %{_libdir}/wx/
%dir %{_libdir}/wx/include/
%dir %{_libdir}/wx/include/gtk2-unicode-release-%{majorminor}/
%dir %{_libdir}/wx/include/gtk2-unicode-release-%{majorminor}/wx/
%dir %{_libdir}/wx/config
%{_libdir}/wx/config/gtk2-unicode-release-%{majorminor}
%{_libdir}/wx/include/gtk2-unicode-release-%{majorminor}/wx/setup.h
%{_libdir}/libwx_gtk2u_adv-%{majorminor}.so
%{_libdir}/libwx_gtk2u_aui-%{majorminor}.so
%{_libdir}/libwx_gtk2u_core-%{majorminor}.so
%{_libdir}/libwx_gtk2u_html-%{majorminor}.so
%{_libdir}/libwx_gtk2u_richtext-%{majorminor}.so
%{_libdir}/libwx_gtk2u_media-%{majorminor}.so
%{_libdir}/libwx_baseu-%{majorminor}.so
%{_libdir}/libwx_baseu_net-%{majorminor}.so
%{_libdir}/libwx_baseu_xml-%{majorminor}.so
# contribs
%{_libdir}/libwx_gtk2u_fl-%{majorminor}.so
%{_libdir}/libwx_gtk2u_gizmos-%{majorminor}.so
%{_libdir}/libwx_gtk2u_gizmos_xrc-%{majorminor}.so
%{_libdir}/libwx_gtk2u_ogl-%{majorminor}.so
%{_libdir}/libwx_gtk2u_plot-%{majorminor}.so
%{_libdir}/libwx_gtk2u_qa-%{majorminor}.so
%{_libdir}/libwx_gtk2u_stc-%{majorminor}.so
%{_libdir}/libwx_gtk2u_svg-%{majorminor}.so
%{_libdir}/libwx_gtk2u_xrc-%{majorminor}.so
#gl
%{_libdir}/libwx_gtk2u_gl-%{majorminor}.so
%{_datadir}/aclocal/*
%{_datadir}/bakefile/
%{_libdir}/wx/config/multiarch-*/
%{_libdir}/wx/include/multiarch-*/
%{_includedir}/multiarch-*/wx-%{majorminor}/wx/defs.h

%files -n %{libglu}
%{_libdir}/libwx_gtk2u_gl-%{majorminor}.so.*


%changelog
* Thu Jan 26 2012 Andrey Bondrov <abondrov@mandriva.org> 2.8.12-6mdv2012.0
+ Revision: 769034
- Remove no longer needed Conflicts

* Tue Jan 24 2012 Andrey Bondrov <abondrov@mandriva.org> 2.8.12-5
+ Revision: 767929
- Drop non-utf8 packages as we don't need them anymore

* Thu Jan 12 2012 Andrey Bondrov <abondrov@mandriva.org> 2.8.12-4
+ Revision: 760322
- Update BuildRequires (add GConf)
- Update BuildRequires (add GStreamer)
- More spec cosmetic cleanups (but still keep RPM4 compatibility)
- Build wx media library, don't build non-utf8 devel package

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix casting issue breaking build (P10)

* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.8.12-3
+ Revision: 702755
- rebuild

* Wed Jun 22 2011 Funda Wang <fwang@mandriva.org> 2.8.12-2
+ Revision: 686699
- do not promote ldflags in config

* Sat May 07 2011 Funda Wang <fwang@mandriva.org> 2.8.12-1
+ Revision: 672191
- new version 2.8.12

* Sat May 07 2011 Funda Wang <fwang@mandriva.org> 2.8.11-4
+ Revision: 672153
- fix multiarch usage

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Sat Jan 01 2011 Funda Wang <fwang@mandriva.org> 2.8.11-3mdv2011.0
+ Revision: 626970
- tighten BR

* Fri Aug 13 2010 Götz Waschk <waschk@mandriva.org> 2.8.11-2mdv2011.0
+ Revision: 569378
- fix plugin directory for 64 bit
- use our optflags and enable no-strict-aliasing
- disable crash handler
- readd translations
- enable grid for Unicode version
- remove Mandriva linker flags from wx-config (bug #44936)
- spec file cleanup

* Mon Jul 26 2010 Götz Waschk <waschk@mandriva.org> 2.8.11-1mdv2011.0
+ Revision: 560863
- new version
- drop merged patches

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8.10-6mdv2010.1
+ Revision: 488812
- rebuilt against libjpeg v8

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8.10-5mdv2010.1
+ Revision: 488616
- P9: security fix for CVE-2009-3560
- P2: security fix related to CVE-2009-2625

* Sat Aug 22 2009 Oden Eriksson <oeriksson@mandriva.com> 2.8.10-3mdv2010.0
+ Revision: 419407
- try to build against system expat

* Mon Aug 17 2009 Oden Eriksson <oeriksson@mandriva.com> 2.8.10-2mdv2010.0
+ Revision: 417197
- fix build
- rebuilt against libjpeg v7

  + Funda Wang <fwang@mandriva.org>
    - sync whe fedora patches

* Mon May 04 2009 Götz Waschk <waschk@mandriva.org> 2.8.10-1mdv2010.0
+ Revision: 371660
- new version
- enable grid widget

* Mon Feb 23 2009 Götz Waschk <waschk@mandriva.org> 2.8.9-3mdv2009.1
+ Revision: 344037
- drop format string patch and disable werror

* Tue Feb 17 2009 Götz Waschk <waschk@mandriva.org> 2.8.9-2mdv2009.1
+ Revision: 341481
- fix format strings
- update license
- enable graphics_ctx (bug #47892)

* Sun Oct 12 2008 Funda Wang <fwang@mandriva.org> 2.8.9-1mdv2009.1
+ Revision: 292755
- New version 2.8.9

  + Götz Waschk <waschk@mandriva.org>
    - fix license

* Thu Jul 10 2008 Oden Eriksson <oeriksson@mandriva.com> 2.8.8-1mdv2009.0
+ Revision: 233373
- 2.8.8
- fix linkage (-lX11)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Feb 07 2008 Götz Waschk <waschk@mandriva.org> 2.8.7-1mdv2008.1
+ Revision: 163590
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 09 2007 Götz Waschk <waschk@mandriva.org> 2.8.6-1mdv2008.1
+ Revision: 96165
- new version
- drop patch 0

  + Funda Wang <fwang@mandriva.org>
    - More clearly provides for develpackages

* Sun Jul 01 2007 Götz Waschk <waschk@mandriva.org> 2.8.4-3mdv2008.0
+ Revision: 46337
- fix wxgtku too (Pascal Terjan)

* Tue Jun 26 2007 Götz Waschk <waschk@mandriva.org> 2.8.4-2mdv2008.0
+ Revision: 44739
- fix for new gslice

* Tue May 22 2007 Götz Waschk <waschk@mandriva.org> 2.8.4-1mdv2008.0
+ Revision: 29866
- new version


* Thu Mar 22 2007 Götz Waschk <waschk@mandriva.org> 2.8.2-1mdv2007.1
+ Revision: 147908
- new version

* Fri Feb 16 2007 Götz Waschk <waschk@mandriva.org> 2.8.0-2mdv2007.1
+ Revision: 121674
- add more docs
- add the demos
- make the samples build easier
- clean conflicts

* Wed Dec 20 2006 Götz Waschk <waschk@mandriva.org> 2.8.0-1mdv2007.1
+ Revision: 100497
- unpack patch
- Import wxgtk2.8

* Wed Dec 20 2006 Götz Waschk <waschk@mandriva.org> 2.8.0-1mdv2007.1
- update file list
- drop patch 1
- add conflicts
- New version 2.8.0

* Wed Aug 16 2006 Götz Waschk <waschk@mandriva.org> 2.7.0-2mdv2007.0
- fix conflicts

* Tue Aug 08 2006 Götz Waschk <waschk@mandriva.org> 2.7.0-1mdv2007.0
- new major
- drop patch 2
- rediff patches 1,8
- New release 2.7.0

* Tue Jun 27 2006 Götz Waschk <waschk@mandriva.org> 2.6.3-7mdv2007.0
- add another conflict

* Tue Jun 27 2006 Charles A Edwards <eslrahc@mandriva.org> 2.6.3-6mdv2007.0
- rebuild again for libpng

* Wed Jun 21 2006 Götz Waschk <waschk@mandriva.org> 2.6.3-5mdv2007.0
- add even more conflicts

* Mon Jun 19 2006 Stefan van der Eijk <stefan@eijk.nu> 2.6.3-1mdv2007.0
- rebuild for png

* Sun Jun 18 2006 Götz Waschk <waschk@mandriva.org> 2.6.3-3mdv2007.0
- add more conflicts
- fix buildrequires

* Wed Jun 14 2006 Oden Eriksson <oeriksson@mandriva.com> 2.6.3-2mdv2007.0
- fix deps

* Fri Mar 31 2006 Götz Waschk <waschk@mandriva.org> 2.6.3-1mdk
- drop patch 3
- New release 2.6.3

* Thu Oct 20 2005 Götz Waschk <waschk@mandriva.org> 2.6.2-2mdk
- fix crash in the unicode version

* Wed Oct 12 2005 Götz Waschk <waschk@mandriva.org> 2.6.2-1mdk
- update file list
- New release 2.6.2

* Sat Jun 18 2005 Götz Waschk <waschk@mandriva.org> 2.6.1-1mdk
- New release 2.6.1

* Fri Jun 10 2005 Götz Waschk <waschk@mandriva.org> 2.6.0-4mdk
- backport support

* Sat May 07 2005 Götz Waschk <waschk@mandriva.org> 2.6.0-3mdk
- fix devel provides (neoclust)

* Sat Apr 30 2005 Götz Waschk <waschk@mandriva.org> 2.6.0-2mdk
- fix buildrequires
- add unicode build

* Tue Apr 26 2005 Götz Waschk <waschk@mandriva.org> 2.6.0-1mdk
- update buildrequires
- enable sdl
- rediff patch 8
- drop patches 3,4,5,6,7,9
- New release 2.6.0

* Sun Feb 20 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.5.3-6mdk
- Patch9: fix configure check for va_copy

* Mon Feb 07 2005 Götz Waschk <waschk@linux-mandrake.com> 2.5.3-5mdk
- fix wx-config script for the multiarch mess

* Fri Feb 04 2005 Götz Waschk <waschk@linux-mandrake.com> 2.5.3-4mdk
- fix multiarch config mess

* Mon Jan 31 2005 Pascal Terjan <pterjan@mandrake.org> 2.5.3-3mdk
- Add multiarch devel support

* Fri Jan 07 2005 Pascal Terjan <pterjan@mandrake.org> 2.5.3-2mdk
- MDKSA-2005:002

* Tue Nov 09 2004 Götz Waschk <waschk@linux-mandrake.com> 2.5.3-1mdk
- fix file list
- new major
- rediff patches 1,2
- drop patch 0
- New release 2.5.3

* Fri Jul 09 2004 Götz Waschk <waschk@linux-mandrake.com> 2.5.1-5mdk
- lib64 fix
- fix devel package group

* Tue Jun 08 2004 Götz Waschk <waschk@linux-mandrake.com> 2.5.1-4mdk
- patch for new g++

* Sat Apr 10 2004 Götz Waschk <waschk@linux-mandrake.com> 2.5.1-3mdk
- fix compatibility with gtk+ 2.4

* Fri Apr 09 2004 Götz Waschk <waschk@linux-mandrake.com> 2.5.1-2mdk
- don't provide wxGTK2.5 in the library package

* Fri Apr 09 2004 Götz Waschk <waschk@linux-mandrake.com> 2.5.1-1mdk
- fix name in the description
- add docs
- fix configure call
- use parallel make
- fix buildrequires
- add contribs
- fix major
- drop unused patch
- fix url
- new version

