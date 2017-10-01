from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy
import sys
import os


with open('README.md') as f:
    readme = f.read()


with open('LICENSE') as f:
    license = f.read()


exec(open('src/coldatoms/version.py').read())


extra_compile_args = [
    '-DDSFMT_MEXP=19937'
    ]
if 'win' in sys.platform:
    if os.environ['PYTHON_ARCH'] == '64':
        extra_compile_args += [
            '-DHAVE_SSE2'
            ]
else:
    extra_compile_args += [
        '-DHAVE_SSE2',
        '-std=c99',
        '-ffast-math',
        '-ftree-vectorize',
        '-msse4']

extra_link_args = []

coldatoms_lib = cythonize([Extension(
    'coldatoms_lib.coldatoms_lib',
    sources=['src/coldatoms_lib/bend_kick_updater.c',
             'src/coldatoms_lib/forces.c',
             'src/coldatoms_lib/ca_rand.c',
             'src/coldatoms_lib/radiation_pressure.c',
             'src/coldatoms_lib/dSFMT/dSFMT.c',
             'src/coldatoms_lib/coldatoms_lib.pyx'],
    include_dirs=['src/coldatoms_lib/', numpy.get_include()],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args
    )])

packages = find_packages(where='src',
                         exclude=('tests', 'docs', 'examples'))

setup(
    name='coldatoms',
    version=__version__,
    description='Collection of python tools for cold atoms simulations',
    long_description=readme,
    author='Dominic Meiser',
    author_email='dmeiser79@gmail.com',
    url='https://github.com/d-meiser/cold-atoms',
    license=license,
    packages=packages,
    package_dir={'': 'src'},
    ext_modules=coldatoms_lib
)
