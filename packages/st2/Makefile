WHEELDIR ?= /tmp/wheelhouse
ST2_COMPONENT := $(notdir $(CURDIR))
ST2PKG_RELEASE ?= 1
ST2PKG_VERSION ?= $(shell python -c "from $(ST2_COMPONENT) import __version__; print __version__,")

ifneq (,$(wildcard /usr/share/python/st2python/bin/python))
	PATH := /usr/share/python/st2python/bin:$(PATH)
endif

ifneq (,$(wildcard /etc/debian_version))
	DEBIAN := 1
	DESTDIR ?= $(CURDIR)/debian/$(ST2_COMPONENT)
else
	REDHAT := 1
endif

.PHONY: all install wheelhouse
all: install

install: wheelhouse changelog

post_install:
	# post_install is triggered from debian/rules file.
	# Don't call it from makefile install target!
	install -m640 /dev/null $(DESTDIR)/etc/st2/htpasswd
	install -m644 ../conf/st2.package.conf $(DESTDIR)/etc/st2/st2.conf
	install -m644 ../conf/logrotate.conf $(DESTDIR)/etc/logrotate.d/st2
	install -m644 ../st2actions/conf/logging.conf $(DESTDIR)/etc/st2/logging.actionrunner.conf
	install -m644 ../st2actions/conf/syslog.conf $(DESTDIR)/etc/st2/syslog.actionrunner.conf
	install -m644 ../st2api/conf/logging.conf $(DESTDIR)/etc/st2/logging.api.conf
	install -m644 ../st2api/conf/syslog.conf $(DESTDIR)/etc/st2/syslog.api.conf
	install -m644 ../st2auth/conf/logging.conf $(DESTDIR)/etc/st2/logging.auth.conf
	install -m644 ../st2auth/conf/syslog.conf $(DESTDIR)/etc/st2/syslog.auth.conf
	sed -i -r "/args\s*=\s*/s%logs%/var/log/st2%g" $(DESTDIR)/etc/st2/logging.*conf
	sed -i "/\[logger_root\]/,/\[.*\]\|\s*$$/ {s/level=DEBUG/level=INFO/}" $(DESTDIR)/etc/st2/logging.*conf
	sed -i "/\[logger_root\]/,/\[.*\]\|\s*$$/ {s/level=DEBUG/level=INFO/}" $(DESTDIR)/etc/st2/syslog.*conf
ifeq ($(REDHAT),1)
	if [ `/root/scripts/platform_major_version.py` = 7 ]; then sed -i -r 's/virtualenv_opts\s*=.*/virtualenv_opts =/' $(DESTDIR)/etc/st2/st2.conf; fi
endif

populate_version: .stamp-populate_version
.stamp-populate_version:
	# populate version should be run before any pip/setup.py works
	sh ../scripts/populate-version.sh
	touch $@

requirements:
	python ../scripts/fixate-requirements.py -s ../st2*/in-requirements.txt -f ../fixed-requirements.txt

changelog: populate_version
ifeq ($(DEBIAN),1)
	debchange -v $(ST2PKG_VERSION)-$(ST2PKG_RELEASE) -M "automated build version: $(ST2PKG_VERSION)"
endif

wheelhouse: .stamp-wheelhouse
.stamp-wheelhouse: populate_version requirements
	touch $@

# For compatibilty with other packages (since it's a meta package)
bdist_wheel: