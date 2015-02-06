Summary:	Hangul input module for GTK+ 3.x
Name:		imhangul
Version:	3.1.1
Release:	2
License:	GPLv2+
Group:		System/Internationalization
Url:		http://code.google.com/p/imhangul/
Source0:	http://imhangul.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libhangul)
Requires:	locales-ko

%description
Hangul input module for GTK+ 3.x

%files -f im-hangul-3.0.lang
%doc AUTHORS COPYING ChangeLog NEWS README gtkrc
%{_libdir}/gtk-3.0/immodules/*.so

#----------------------------------------------------------------------------

%prep
%setup -q

%build
%configure2_5x --with-gtk-im-module-dir=%{_libdir}/gtk-3.0/immodules/
%make

%install
%makeinstall_std

%find_lang im-hangul-3.0

