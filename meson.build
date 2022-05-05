project('pulseaudio-module-hidl', 'c',
        version : run_command(find_program('git-version-gen'), join_paths(meson.current_source_dir(), '.tarball-version'), check: true).stdout().strip(),
        meson_version : '>= 0.50.0',
        default_options : [ 'c_std=gnu11' ]
        )

cc = meson.get_compiler('c')

configinc = include_directories('.')

pa_c_args = ['-DHAVE_CONFIG_H']

droiddevice = get_option('droid-device')
pa_c_args += ['-DDROID_DEVICE_@0@=1'.format(droiddevice.underscorify().to_upper())]
pa_c_args += ['-DDROID_DEVICE_STRING="@0@"'.format(droiddevice)]
pa_c_args += ['-DLIB_AF_NAME="@0@"'.format(get_option('audioflingerglue-name'))]
pa_c_args += ['-DLIB_AF_BASE_PATH="@0@"'.format(get_option('audioflingerglue-base'))]


# dependencies
droid_headers_dep = dependency('android-headers', required : true)
hybris_dep = dependency('libhardware', version : '>= 0.1.0', required : true)
hybris_common_dep = cc.find_library('hybris-common', required : true)
pulsecore_dep = dependency('pulsecore', version : '>= 14.2', required : true)

pa_version_str = pulsecore_dep.version()
# For tarballs, the first split will do nothing, but for builds in git, we
# split out suffixes when there are commits since the last tag
# (e.g.: v11.99.1-3-gad14bdb24 -> v11.99.1)
version_split = pa_version_str.split('-')[0].split('.')
pa_version_major = version_split[0].split('v')[0]
pa_version_minor = version_split[1]
pa_version_major_minor = pa_version_major + '.' + pa_version_minor

modlibexecdir = get_option('modlibexecdir')
if modlibexecdir == ''
  modlibexecdir = join_paths(get_option('libdir'), 'pulse-' + pa_version_major_minor, 'modules')
endif

cdata = configuration_data()
cdata.set_quoted('PACKAGE', meson.project_name())
cdata.set_quoted('PACKAGE_NAME', meson.project_name())
cdata.set_quoted('PACKAGE_VERSION', pa_version_str)
cdata.set_quoted('VERSION', pa_version_str)

# Atomic operations

if get_option('atomic-arm-memory-barrier')
    cdata.set('ATOMIC_ARM_MEMORY_BARRIER_ENABLED', 1)
endif

need_libatomic_ops = false

atomictest = '''void func() {
  volatile int atomic = 2;
  __sync_bool_compare_and_swap (&atomic, 2, 3);
}
'''

if cc.compiles(atomictest)
  cdata.set('HAVE_ATOMIC_BUILTINS', 1)

  newatomictest = '''void func() {
    int c = 0;
    __atomic_store_n(&c, 4, __ATOMIC_SEQ_CST);
  }
  '''

  if cc.compiles(newatomictest)
    cdata.set('HAVE_ATOMIC_BUILTINS_MEMORY_MODEL', 1)
  endif

elif host_machine.cpu_family() == 'arm'
  if host_machine.system() == 'linux' and get_option('atomic-arm-linux-helpers')
    cdata.set('ATOMIC_ARM_LINUX_HELPERS', 1)
  else
    armatomictest = '''int func() {
      volatile int a=0;
      int o=0, n=1, r;
      asm volatile (
          "ldrex    %0, [%1]\n"
          "subs  %0, %0, %2\n"
          "strexeq %0, %3, [%1]\n"
          : "=&r" (r)
          : "r" (&a), "Ir" (o), "r" (n)
      : "cc");
      return (a==1 ? 0 : -1);
    }
    '''

    if cc.compiles(armatomictest)
      cdata.set('ATOMIC_ARM_INLINE_ASM', 1)
    else
      need_libatomic_ops = true
    endif
  endif # arm && !linux

elif not ['freebsd', 'netbsd'].contains(host_machine.system())
  need_libatomic_ops = true
endif # !atomic helpers && !arm

if need_libatomic_ops
  cc.has_header('atomic_ops.h', required: true)

  cdata.set('AO_REQUIRE_CAS', 1)

  if host_machine.system() != 'windows'
    libatomic_ops_dep = cc.find_library('atomic_ops', required : true)
  else
    libatomic_ops_dep = dependency('', required: false)
  endif
else
  libatomic_ops_dep = dependency('', required: false)
endif

# Headers

# Require audioflingerglue.h

cc.has_header('audioflingerglue/audioflingerglue.h', required : true)

check_headers = [
  'valgrind/memcheck.h',
]

foreach h : check_headers
  if cc.has_header(h)
    define = 'HAVE_' + h.underscorify().to_upper()
    cdata.set(define, 1)
  endif
endforeach

subdir('src')

# Now generate config.h from everything above
configure_file(output : 'config.h', configuration : cdata)

