# This Makefile is part of Offline SHR Manager
#
# global parameters
TITLE=		"Offline SHR Manager"
URL=		"https://projects.openmoko.org/projects/oshyreman/"
VERSION=	"0.0.1"

dist:
	mkdir -p build/ubuntu/DEBIAN
	cp build/control build/ubuntu/DEBIAN/control
	mkdir -p build/ubuntu/usr/bin
	mkdir -p build/ubuntu/opt/oshyreman
	cp *.py COPYING build/ubuntu/opt/oshyreman
	mkdir -p build/ubuntu/opt/oshyreman/gtkgui
	cp gtkgui/*.py build/ubuntu/opt/oshyreman/gtkgui
	mkdir build/ubuntu/bin
	ln -s /opt/oshyreman/oshyreman.py build/ubuntu/bin/oshyreman
	ln -s /opt/oshyreman/oshyreman_gui.py build/ubuntu/bin/oshyreman_gui	
	cd build && dpkg --build ubuntu/ oshyreman-$(VERSION).deb
	rm -rf build/ubuntu

sdist: clean
	tar czf build/oshyreman-src-$(VERSION).tar.gz Makefile COPYING *.py build/control

clean:
	rm -f *.pyc gtkgui/*.pyc
