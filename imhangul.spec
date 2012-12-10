%define version	2.0.0
%define release %mkrel 1

Summary:	Hangul input module for GTK+ 2.x
Name:		imhangul
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Internationalization
URL:		http://kldp.net/projects/imhangul/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

Source0:	http://kldp.net/frs/download.php/2808/%{name}-%{version}.tar.bz2

BuildRequires:	gtk2-devel >= 2.4.0
BuildRequires:	libhangul-devel >= 0.0.10
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


%changelog
* Sat May 28 2011 Funda Wang <fwang@mandriva.org> 2.0.0-1mdv2011.0
+ Revision: 680438
- cleanup spec
- new version 2.0.0

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.15-2mdv2011.0
+ Revision: 611182
- rebuild

* Wed Dec 09 2009 Funda Wang <fwang@mandriva.org> 0.9.15-1mdv2010.1
+ Revision: 475300
- new version 0.9.15

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.9.13-6mdv2010.0
+ Revision: 429505
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.9.13-5mdv2009.0
+ Revision: 247219
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Thierry Vignaud <tv@mandriva.org> 0.9.13-3mdv2008.1
+ Revision: 131821
- fix prereq
- kill re-definition of %%buildroot on Pixel's request
- import imhangul


* Fri Dec 02 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.9.13-2mdk
- fix build on x86_64

* Fri Dec 02 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.9.13-1mdk
- new release

* Thu Feb 24 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.11-1mdk
- new release
- fix csh script (#12193)

* Fri Jul 30 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.10-1mdk
- new release

* Wed Jul 28 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.9-3mdk
- biarch support

* Sat Feb 14 2004 Abel Cheung <deaddog@deaddog.org> 0.9.9-2mdk
- Requires locales-ko

* Sun Feb 08 2004 Abel Cheung <deaddog@deaddog.org> 0.9.9-1mdk
- New version
- Set GTK_IM_MODULES only for korean locales
- Mark startup scripts as config

* Wed Dec 17 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.9.8-1mdk
- from Nicolas Fatoux <nicolas.fatoux@laposte.nt> :
	- mdk adaptation

* Sun Nov 23 2003 Young-Ho,Cha <ganadist@chollian.net> 
- update 0.9.8

* Tue Oct 21 2003 Young-Ho,Cha <ganadist@chollian.net>
- update 0.9.7

* Mon Mar 31 2003 Young-Ho,Cha <ganadist@chollian.net>
- update 0.9.6
- GTK_IM_MODULE default value set hangul2

* Wed Jan 15 2003 Young-Ho,Cha <ganadist@chollian.net>
- update 0.9.5
- rename profile scripts

* Wed Nov 13 2002 Young-Ho,Cha <ganadist@chollian.net>
- remove '=' symbol in csh profile script

* Tue Nov 12 2002 Young-Ho,Cha <ganadist@chollian.net>
- update 0.9.4

* Sat Oct 12 2002 Young-Ho,Cha <ganadist@chollian.net>
- update 0.9.3

* Thu Oct 10 2002 Young-Ho,Cha <ganadist@chollian.net>
- change scripts to work properly

* Wed Sep 11 2002 Young-Ho,Cha <ganadist@chollian.net>
- update 0.9.2

* Mon Aug 19 2002 Young-Ho,Cha <ganadist@chollian.net>
- update 0.9.1

* Fri Aug 16 2002 Young-Ho,Cha <ganadist@chollian.net>
- use macros
- add profile scripts

* Mon Jul 22 2002 Lee, Kwan-hong <sorcerer@jerimo.org>
- Make RPM package
