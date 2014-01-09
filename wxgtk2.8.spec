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
Release:	12
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
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	tiff-devel
BuildRequires:	bison, flex
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
%{_libdir}/wx/config/multiarch-*/gtk2-unicode-release-%{majorminor}
%{_libdir}/wx/include/multiarch-*/gtk2-unicode-release-%{majorminor}
%{_includedir}/multiarch-*/wx-%{majorminor}/wx/defs.h

%files -n %{libglu}
%{_libdir}/libwx_gtk2u_gl-%{majorminor}.so.*

