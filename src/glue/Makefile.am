AM_LIBADD = \
	$(PULSEAUDIO_LIBS) \
	$(HYBRIS_LIBS)
AM_CFLAGS = \
	$(DROID_DEVICE_CFLAGS) \
	$(PULSEAUDIO_CFLAGS) \
	$(DROIDHEADERS_CFLAGS) \
	$(HYBRIS_CFLAGS) \
	$(LIB_AF_CFLAGS) \
	-DPULSEAUDIO_VERSION=@PA_MAJOR@ \
	-I$(top_srcdir)/src/glue


modlibexec_LTLIBRARIES = module-droid-glue.la

noinst_HEADERS = module-droid-glue-symdef.h

module_droid_glue_la_SOURCES = /usr/share/audioflingerglue/hybris.c module-droid-glue.c
module_droid_glue_la_LDFLAGS = -module -avoid-version -Wl,-no-undefined -Wl,-z,noexecstack -lhybris-common
module_droid_glue_la_LIBADD = $(AM_LIBADD) -lm
module_droid_glue_la_CFLAGS = $(AM_CFLAGS) -I/usr/include/audioflingerglue
