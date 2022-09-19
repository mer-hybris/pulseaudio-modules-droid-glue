module_droid_glue = shared_module('module-droid-glue',
  ['module-droid-glue.c', '/usr/share/audioflingerglue/hybris.c'],
  include_directories : [configinc],
  c_args : [pa_c_args, '-I/usr/include/audioflingerglue', '-DPA_MODULE_NAME=module_droid_glue'],
  install : true,
  install_dir : modlibexecdir,
  dependencies : [
    droid_headers_dep,
    hybris_dep,
    hybris_common_dep,
    pulsecore_dep
  ],
  name_prefix : ''
)
