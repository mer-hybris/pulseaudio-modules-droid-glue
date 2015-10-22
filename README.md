PulseAudio Droid glue module
============================

module-droid-glue
-----------------

The purpose of this module is to forward calls made to AudioFlinger to
active hw module. This means that glue module cannot be loaded independently,
it needs to have module-droid-card or module-droid-{sink,source} or whatever
module loaded beforehand that parses droid configuration and loads the hw
module to PulseAudio global object.
