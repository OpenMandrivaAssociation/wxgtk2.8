%define oname wxGTK
%define fname wxGTK
%define majorminor	2.8
%define name		wxgtk%majorminor
%define version 2.8.4
%define	major		%majorminor
%define release %mkrel 4

%define	libname %mklibname wxgtk %{major}
%define	libnamedev %mklibname -d wxgtk %{major}
%define libgl	%mklibname wxgtkgl %{major}

%define	libnameu %mklibname wxgtku %{major}
%define	libnameudev %mklibname -d wxgtku %{major}
%define libglu	%mklibname wxgtkglu %{major}
#fixed2
%{?!mkrel:%define mkrel(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

Summary:	GTK+ port of the wxWidgets library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://www.wxwindows.org
# http://wxwindows.sourceforge.net/snapshots/wx-cvs-20030817.tar.bz2
Source:		http://prdownloads.sourceforge.net/wxwindows/%fname-%version.tar.bz2
# gw fix from Ubuntu
Patch:		wxgtk-2.8-new-gslice.patch
Patch8:		wxWidgets-2.7.0-multiarch-includes.patch
Buildrequires:	libpng-devel
Buildrequires:	zlib-devel
Buildrequires:	libgnomeprintui-devel
Buildrequires:	libSDL-devel
Buildrequires:	libjpeg-devel
Buildrequires:	bison, flex
Buildrequires:	libtiff-devel
BuildRequires:  libmesaglu-devel
BuildRequires:  cppunit-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
#Conflicts: wxGTK2.6 wxGTK2.5 wxGTK
Conflicts: %mklibname wx_base2.4_ 0

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
%patch -p1
%patch8 -p1 -b .multiarch
cd %oname-%version
%patch -p1
%patch8 -p1

find samples demos -name .cvsignore -exec rm {} \;

%build
export LDFLAGS=-L%_prefix/X11R6/%_lib
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
	--enable-optimise \
	\
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
	--enable-textdlg

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
	\
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
	--enable-textdlg
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

%post   -n %{libname}	-p /sbin/ldconfig
%postun -n %{libname}	-p /sbin/ldconfig
%post   -n %{libgl}	-p /sbin/ldconfig
%postun -n %{libgl}	-p /sbin/ldconfig

%post   -n %{libnameu}	-p /sbin/ldconfig
%postun -n %{libnameu}	-p /sbin/ldconfig
%post   -n %{libglu}	-p /sbin/ldconfig
%postun -n %{libglu}	-p /sbin/ldconfig

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
