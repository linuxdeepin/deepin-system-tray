#!/user/binenv python

from distutils.core import setup, Extension
import commands

def pkg_config_cflags(pkgs):
    '''List all include paths that output by `pkg-config --cflags pkgs`'''
    return map(lambda path: path[2::], commands.getoutput('pkg-config --cflags-only-I %s' % (' '.join(pkgs))).split())
    
cairo_mod = Extension('vtk_cairo_blur',
                include_dirs = pkg_config_cflags(['cairo', 'pygobject-2.0']),
                libraries = ['cairo', 'pthread', 'glib-2.0'],
                sources = ['cairo_blur.c'])
MOD = "dtk_cairo_blur"
setup(name=MOD, ext_modules=[cairo_mod])
