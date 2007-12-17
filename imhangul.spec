%define version	0.9.13
%define release %mkrel 3

Summary:	Hangul input module for GTK+ 2.x
Name:		imhangul
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Internationalization
URL:		http://kldp.net/projects/imhangul/

Source0:	http://kldp.net/frs/download.php/2808/%{name}-%{version}.tar.bz2

BuildRequires:	gtk2-devel >= 2.4.0
Requires(post,preun):		%_bindir/gtk-query-immodules-2.0
Requires:	gtk+2.0 >= 2.4.4-2mdk
Requires:	locales-ko

%description
Hangul input module for GTK+ 2.x

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/imhangul.sh <<EOF
#!/bin/sh
if echo "\$LC_CTYPE" | grep -q '^ko'; then
	export GTK_IM_MODULE=hangul2
	if [ -n "\$HANGUL_KEYBOARD_TYPE" ] ; then
		case "\$HANGUL_KEYBOARD_TYPE" in
			"3"|"389"|"3FINAL")
				export GTK_IM_MODULE=hangul3f
				;;
			"390")
				export GTK_IM_MODULE=hangul39
				;;
		"3NOSHIFT")
		    export GTK_IM_MODULE=hangul3s
		    ;;
		"2"| *)
		    export GTK_IM_MODULE=hangul2
		    ;;
		esac
	fi
fi
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/imhangul.csh <<EOF
#!/bin/csh
if (\$?LC_CTYPE) then
	if (\`echo "\$LC_CTYPE" | grep -q '^ko'\`) then
		setenv GTK_IM_MODULE hangul2
		if (\$?HANGUL_KEYBOARD_TYPE) then
			switch ($HANGUL_KEYBOARD_TYPE)
				case 3:
				case 389:
				case 3FINAL:
					setenv GTK_IM_MODULE hangul3f
					breaksw
				case 390:
					setenv GTK_IM_MODULE hangul39
					breaksw
				case 3NOSHIFT:
					setenv GTK_IM_MODULE hangul3s
					breaksw
				case 2:
				case *:
					setenv GTK_IM_MODULE hangul2
					breaksw
			endsw
		endif
	endif
endif
EOF

chmod 755 %{buildroot}%{_sysconfdir}/profile.d/imhangul*

# (tv) fix build on x86_64:
%ifarch x86_64
mkdir -p %{buildroot}%_libdir
mv %{buildroot}{%_prefix/lib,%_libdir}/gtk-2.0/
%endif

# remove unneeded file
rm -f %{buildroot}%{_libdir}/gtk-2.0/immodules/*.la

%find_lang im-hangul

%clean
rm -rf %{buildroot}

%files -f im-hangul.lang
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING ChangeLog NEWS README gtkrc
%config(noreplace) %{_sysconfdir}/profile.d/imhangul*
%{_libdir}/gtk-2.0/immodules/*.so


%post
%{_bindir}/gtk-query-immodules-2.0 %_lib > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun
if [ $1 -eq 0 ]; then
  %{_bindir}/gtk-query-immodules-2.0 %_lib > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib
fi

