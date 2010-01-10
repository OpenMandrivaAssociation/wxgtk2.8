%define oname wxGTK
%define fname wxGTK
%define majorminor	2.8
%define name		wxgtk%majorminor
%define version 2.8.10
%define	major		%majorminor
%define release %mkrel 5

%define	libname %mklibname wxgtk %{major}
%define	libnamedev %mklibname -d wxgtk %{major}
%define libgl	%mklibname wxgtkgl %{major}

%define	libnameu %mklibname wxgtku %{major}
%define	libnameudev %mklibname -d wxgtku %{major}
%define libglu	%mklibname wxgtkglu %{major}

Summary:	GTK+ port of the wxWidgets library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	wxWidgets Library Licence
Group:		System/Libraries
URL:		http://www.wxwidgets.org/
Source0:	http://prdownloads.sourceforge.net/wxwindows/%fname-%version.tar.bz2
# http://trac.wxwidgets.org/ticket/10883
Patch0:         %{oname}-2.8.10-gsocket.patch
# http://trac.wxwidgets.org/ticket/10993
Patch1:         %{oname}-2.8.10-CVE-2009-2369.patch
Patch2:		wxGTK-2.8.10-CVE-2009-XXXX.diff
Patch3:		wxGTK-lX11_linkage_fix.diff
Patch8:		wxWidgets-2.7.0-multiarch-includes.patch
Patch9:		wxGTK-2.8.8-CVE-2009-3560.diff
Buildrequires:	libpng-devel
Buildrequires:	libgnomeprintui-devel
Buildrequires:	libSDL-devel
Buildrequires:	libjpeg-devel
Buildrequires:	bison, flex
Buildrequires:	libtiff-devel
BuildRequires:  libmesaglu-devel
BuildRequires:  cppunit-devel
BuildRequires:  X11-devel
BuildRequires:  expat-devel
#Conflicts: wxGTK2.6 wxGTK2.5 wxGTK
Conflicts: %mklibname wx_base2.4_ 0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
wxWidgets is a free C++ library for cross-platform GUI development.
With wxWidgets, you can create applications for different GUIs (GTK+,
Motif/LessTif, MS Windows, Mac) from the same source code.

%package -n %libname
Group:		System/Libraries
Summary: 	Base shared library part of wxGTK
Requires:	%name >= %version

%description -n %libname
wxWidgets is a free C++ library for cross-platform GUI development.
With wxWidgets, you can create applications for different GUIs (GTK+,
Motif/LessTif, MS Windows, Mac) from the same source code.

This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{libnamedev}
Summary:	Header files and development documentation for wxGTK
Group:		Development/C++
Requires:	%{libname} = %version
Requires:	%{libgl} = %version
Provides:	wxGTK-devel = %version-%release
Provides:	wxGTK%{majorminor}-devel = %version-%release
Provides:	libwxgtk%majorminor-devel = %version-%release
Provides:	libwxgtk-devel = %version-%release
Conflicts:	wxGTK6-devel wxGTK2.2-devel wxGTK2.3_1-devel
Conflicts:	libwxBase0-devel
Conflicts:	%mklibname wxgtk 2.4 -d
Conflicts:	%mklibname wxgtk 2.5_3 -d
Conflicts:	%mklibname wxgtk 2.6 -d
Conflicts:	%mklibname wxgtku 2.6 -d
Conflicts:	%mklibname wx_base2.4_ 0 -d

%description -n %{libnamedev}
Header files for wxGTK, the GTK+ port of the wxWidgets library.

%package  -n %{libgl}
Summary:	GTK+ port of the wxWidgets library, OpenGl add-on
Group:		System/Libraries
Provides:	wxGTK-gl = %version-%release
Provides:	wxGTK%{majorminor}-gl = %version-%release

%description -n %{libgl}
OpenGl add-on library for wxGTK, the GTK+ port of the wxWidgets library.

%package -n %libnameu
Group:		System/Libraries
Summary: 	Base shared library part of wxGTK - Unicode enabled
Requires:	%name >= %version

%description -n %libnameu
wxWidgets is a free C++ library for cross-platform GUI development.
With wxWidgets, you can create applications for different GUIs (GTK+,
Motif/LessTif, MS Windows, Mac) from the same source code.

This package contains the library needed to run programs dynamically
linked with the unicode enabled version of %{name}.

%package -n %{libnameudev}
Summary:	Header files and development documentation for wxGTK - unicode
Group:		Development/C++
Requires:	%{libnameu} = %version
Requires:	%{libglu} = %version
Provides:	libwxgtku-devel = %version-%release
Provides:	wxgtku-devel = %version-%release
Provides:	wxgtku%majorminor-devel = %version-%release
Provides:	libwxgtku%majorminor-devel = %version-%release
Conflicts:	%libname-devel < %version-%release
Conflicts:	%libname-devel > %version-%release
Conflicts:	%mklibname wxgtk 2.4 -d
Conflicts:	%mklibname wxgtk 2.5_3 -d
Conflicts:	%mklibname wxgtk 2.6 -d
Conflicts:	%mklibname wxgtku 2.6 -d
Conflicts:	%mklibname wx_base2.4_ 0 -d

%description -n %{libnameudev}
Header files for the unicode enabled version of wxGTK, the GTK+ port of
the wxWidgets library.

%package  -n %{libglu}
Summary:	GTK+ port of the wxWidgets library, OpenGl add-on - unicode
Group:		System/Libraries

%description -n %{libglu}
OpenGl add-on library for the unicode enabled version of wxGTK, the
GTK+ port of the wxWidgets library.

%prep
%setup -q -n %oname-%version -a 0
%patch0 -p1 -b .gsocket
%patch1 -p0 -b .CVE-2009-2369
%patch2 -p0 -b .CVE-2009-XXXX
%patch3 -p1
%patch8 -p1 -b .multiarch
%patch9 -p0 -b .CVE-2009-3560
cd %oname-%version
%patch0 -p1 -b .gsocket
%patch1 -p0 -b .CVE-2009-2369
%patch2 -p0 -b .CVE-2009-XXXX
%patch3 -p1
%patch8 -p1
%patch9 -p0 -b .CVE-2009-3560

find samples demos -name .cvsignore -exec rm {} \;

%build
#gw 2.8.9 doesn't build:
%define _disable_ld_no_undefined 1
%define Werror_cflags %nil

%configure2_5x \
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
	--with-expat=sys \
	--enable-optimise \
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
	--enable-grid

%make
cd contrib
%make
cd ..
#gw prepare samples
cd demos
make clean
rm -f makefile* demos.bkl
cd ../samples
make clean
rm -f makefile* samples.bkl
cd ..
find demos samples -name Makefile|xargs perl -pi -e 's^CXXC =.*^CXXC=\$(CXX) `wx-config --cflags`^'
find demos samples -name Makefile|xargs perl -pi -e 's^EXTRALIBS =.*^EXTRALIBS=^'
find demos samples -name Makefile|xargs perl -pi -e 's^SAMPLES_RPATH_FLAG =.*^SAMPLES_RPATH_FLAG=^'

cd %oname-%version
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
	--enable-optimise \
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
	--enable-graphics_ctx
%make
cd contrib
%make

%install
rm -rf %buildroot wxstd.lang wxmsw.lang
%makeinstall
%find_lang wxstd
%find_lang wxmsw
cat wxmsw.lang >> wxstd.lang
cd contrib
%makeinstall
cd ..
mv %buildroot%_bindir/wxrc-%{majorminor} %buildroot%_bindir/wxrc-%{majorminor}-ansi
#gw fix broken symlink
rm -f %buildroot%_bindir/{wx-config,wxrc}
###
cd %oname-%version
%makeinstall
cd contrib
%makeinstall
mv %buildroot%_bindir/wxrc-%{majorminor} %buildroot%_bindir/wxrc-%{majorminor}-unicode
###
#gw fix broken symlink
rm -f %buildroot%_bindir/{wx-config,wxrc}
ln -sf %_libdir/wx/config/gtk2-ansi-release-%{majorminor} %buildroot%_bindir/wx-config-ansi
ln -sf %_libdir/wx/config/gtk2-unicode-release-%{majorminor} %buildroot%_bindir/wx-config-unicode


%if %mdkversion >= 1020
# multiarch devel
%multiarch_binaries $RPM_BUILD_ROOT%{_libdir}/wx/config/gtk2-{ansi,unicode}-release-%{majorminor}
#gw this breaks /usr/bin/wx-config
mkdir %buildroot%multiarch_bindir
ln -s %{_libdir}/wx/config/%multiarch_platform/gtk2-ansi-release-%{majorminor} %buildroot%multiarch_bindir/wx-config-ansi
ln -s %{_libdir}/wx/config/%multiarch_platform/gtk2-unicode-release-%{majorminor} %buildroot%multiarch_bindir/wx-config-unicode
%multiarch_includes $RPM_BUILD_ROOT%{_libdir}/wx/include/gtk2-{ansi,unicode}-release-%{majorminor}/wx/setup.h
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/wx-%{majorminor}/wx/defs.h
%endif

%clean
rm -rf %buildroot

%if %mdkversion < 200900
%post   -n %{libname}	-p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname}	-p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%post   -n %{libgl}	-p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libgl}	-p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post   -n %{libnameu}	-p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libnameu}	-p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%post   -n %{libglu}	-p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libglu}	-p /sbin/ldconfig
%endif

%post -n %libnamedev
update-alternatives --install %{_bindir}/wx-config wx-config %{_libdir}/wx/config/gtk2-ansi-release-%{majorminor} 20 --slave %_bindir/wxrc wxrc %_bindir/wxrc-%{majorminor}-ansi
%postun -n %libnamedev
if [ "$1" = "0" ]; then
  update-alternatives --remove wx-config %{_libdir}/wx/config/gtk2-ansi-release-%{majorminor} 
fi

%post -n %libnameudev
update-alternatives --install %{_bindir}/wx-config wx-config %{_libdir}/wx/config/gtk2-unicode-release-%{majorminor} 15 --slave %_bindir/wxrc wxrc %_bindir/wxrc-%{majorminor}-unicode
%postun -n %libnameudev
if [ "$1" = "0" ]; then
  update-alternatives --remove wx-config %{_libdir}/wx/config/gtk2-unicode-release-%{majorminor} 
fi

%files -f wxstd.lang
%defattr(-,root,root,-)
%doc *.txt

%files -n %libname
%defattr(-,root,root,-)
%_libdir/libwx_gtk2_adv-%{majorminor}.so.*
%_libdir/libwx_gtk2_aui-%{majorminor}.so.*
%_libdir/libwx_gtk2_core-%{majorminor}.so.*
%_libdir/libwx_gtk2_html-%{majorminor}.so.*
%_libdir/libwx_gtk2_richtext-%{majorminor}.so.*
%_libdir/libwx_base-%majorminor.so.*
%_libdir/libwx_base_net-%majorminor.so.*
%_libdir/libwx_base_xml-%majorminor.so.*
# contribs
%_libdir/libwx_gtk2_fl-%{majorminor}.so.*
%_libdir/libwx_gtk2_gizmos-%{majorminor}.so.*
%_libdir/libwx_gtk2_gizmos_xrc-%{majorminor}.so.*
%_libdir/libwx_gtk2_ogl-%{majorminor}.so.*
%_libdir/libwx_gtk2_plot-%{majorminor}.so.*
%_libdir/libwx_gtk2_qa-%{majorminor}.so.*
%_libdir/libwx_gtk2_stc-%{majorminor}.so.*
%_libdir/libwx_gtk2_svg-%{majorminor}.so.*
%_libdir/libwx_gtk2_xrc-%{majorminor}.so.*

%files -n %libnameu
%defattr(-,root,root,-)
%_libdir/libwx_gtk2u_adv-%{majorminor}.so.*
%_libdir/libwx_gtk2u_aui-%{majorminor}.so.*
%_libdir/libwx_gtk2u_core-%{majorminor}.so.*
%_libdir/libwx_gtk2u_html-%{majorminor}.so.*
%_libdir/libwx_gtk2u_richtext-%{majorminor}.so.*
%_libdir/libwx_baseu-%majorminor.so.*
%_libdir/libwx_baseu_net-%majorminor.so.*
%_libdir/libwx_baseu_xml-%majorminor.so.*
# contribs
%_libdir/libwx_gtk2u_fl-%{majorminor}.so.*
%_libdir/libwx_gtk2u_gizmos-%{majorminor}.so.*
%_libdir/libwx_gtk2u_gizmos_xrc-%{majorminor}.so.*
%_libdir/libwx_gtk2u_ogl-%{majorminor}.so.*
%_libdir/libwx_gtk2u_plot-%{majorminor}.so.*
%_libdir/libwx_gtk2u_qa-%{majorminor}.so.*
%_libdir/libwx_gtk2u_stc-%{majorminor}.so.*
%_libdir/libwx_gtk2u_svg-%{majorminor}.so.*
%_libdir/libwx_gtk2u_xrc-%{majorminor}.so.*

%files -n %{libnamedev}
%defattr(-,root,root,-)
%doc samples/
%doc docs/
%doc demos/
%{_bindir}/wx-config-ansi
%{_bindir}/wxrc-*ansi
%if %mdkversion >= 1020
%{multiarch_bindir}/wx-config-ansi
%endif
%{_includedir}/wx-%{majorminor}/
%dir %{_libdir}/wx/
%dir %{_libdir}/wx/include/
%dir %{_libdir}/wx/include/gtk2-ansi-release-%{majorminor}/
%dir %{_libdir}/wx/include/gtk2-ansi-release-%{majorminor}/wx/
%dir %{_libdir}/wx/config
%{_libdir}/wx/config/gtk2-ansi-release-%{majorminor}
%{_libdir}/wx/include/gtk2-ansi-release-%{majorminor}/wx/setup.h
%_libdir/libwx_gtk2_adv-%{majorminor}.so
%_libdir/libwx_gtk2_aui-%{majorminor}.so
%_libdir/libwx_gtk2_core-%{majorminor}.so
%_libdir/libwx_gtk2_html-%{majorminor}.so
%_libdir/libwx_gtk2_richtext-%{majorminor}.so
%_libdir/libwx_base-%majorminor.so
%_libdir/libwx_base_net-%majorminor.so
%_libdir/libwx_base_xml-%majorminor.so
# contribs
%_libdir/libwx_gtk2_fl-%{majorminor}.so
%_libdir/libwx_gtk2_gizmos-%{majorminor}.so
%_libdir/libwx_gtk2_gizmos_xrc-%{majorminor}.so
%_libdir/libwx_gtk2_ogl-%{majorminor}.so
%_libdir/libwx_gtk2_plot-%{majorminor}.so
%_libdir/libwx_gtk2_qa-%{majorminor}.so
%_libdir/libwx_gtk2_stc-%{majorminor}.so
%_libdir/libwx_gtk2_svg-%{majorminor}.so
%_libdir/libwx_gtk2_xrc-%{majorminor}.so
#gl
%_libdir/libwx_gtk2_gl-%{majorminor}.so
%_datadir/aclocal/*
%_datadir/bakefile/
%if %mdkversion >= 1020
%multiarch %{_libdir}/wx/config/multiarch-*/gtk2-ansi-release-%{majorminor}
%multiarch %{_libdir}/wx/include/multiarch-*/gtk2-ansi-release-%{majorminor}
%multiarch %{_includedir}/multiarch-*/wx-%{majorminor}/wx/defs.h
%endif

%files -n %{libnameudev}
%defattr(-,root,root,-)
%doc samples/
%doc docs/
%doc demos/
%{_bindir}/wx-config-unicode
%{_bindir}/wxrc-*unicode
%if %mdkversion >= 1020
%{multiarch_bindir}/wx-config-unicode
%endif
%{_includedir}/wx-%{majorminor}/
%dir %{_libdir}/wx/
%dir %{_libdir}/wx/include/
%dir %{_libdir}/wx/include/gtk2-unicode-release-%{majorminor}/
%dir %{_libdir}/wx/include/gtk2-unicode-release-%{majorminor}/wx/
%dir %{_libdir}/wx/config
%{_libdir}/wx/config/gtk2-unicode-release-%{majorminor}
%{_libdir}/wx/include/gtk2-unicode-release-%{majorminor}/wx/setup.h
%_libdir/libwx_gtk2u_adv-%{majorminor}.so
%_libdir/libwx_gtk2u_aui-%{majorminor}.so
%_libdir/libwx_gtk2u_core-%{majorminor}.so
%_libdir/libwx_gtk2u_html-%{majorminor}.so
%_libdir/libwx_gtk2u_richtext-%{majorminor}.so
%_libdir/libwx_baseu-%majorminor.so
%_libdir/libwx_baseu_net-%majorminor.so
%_libdir/libwx_baseu_xml-%majorminor.so
# contribs
%_libdir/libwx_gtk2u_fl-%{majorminor}.so
%_libdir/libwx_gtk2u_gizmos-%{majorminor}.so
%_libdir/libwx_gtk2u_gizmos_xrc-%{majorminor}.so
%_libdir/libwx_gtk2u_ogl-%{majorminor}.so
%_libdir/libwx_gtk2u_plot-%{majorminor}.so
%_libdir/libwx_gtk2u_qa-%{majorminor}.so
%_libdir/libwx_gtk2u_stc-%{majorminor}.so
%_libdir/libwx_gtk2u_svg-%{majorminor}.so
%_libdir/libwx_gtk2u_xrc-%{majorminor}.so
#gl
%_libdir/libwx_gtk2u_gl-%{majorminor}.so
%_datadir/aclocal/*
%_datadir/bakefile/
%if %mdkversion >= 1020
%multiarch %{_libdir}/wx/config/multiarch-*/gtk2-unicode-release-%{majorminor}
%multiarch %{_libdir}/wx/include/multiarch-*/gtk2-unicode-release-%{majorminor}
%multiarch %{_includedir}/multiarch-*/wx-%{majorminor}/wx/defs.h
%endif

%files -n %{libgl}
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk2_gl-%majorminor.so.*

%files -n %{libglu}
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk2u_gl-%majorminor.so.*
