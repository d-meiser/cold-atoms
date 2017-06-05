from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy


with open('README.md') as f:
    readme = f.read()


with open('LICENSE') as f:
    license = f.read()


# TODO(Dominic): The following flags are suitable for gcc and clang. Down the
# road this will have to be special cased for the different toolchains. Also,
# the ISA is hardwired for now.
extra_compile_args = ['-std=c99', '-ffast-math', '-ftree-vectorize', '-msse4']
extra_link_args = []

coldatoms_lib = cythonize([Extension(
    'coldatoms_lib.coldatoms_lib',
    sources=['src/coldatoms_lib/bend_kick_updater.c',
             'src/coldatoms_lib/forces.c',
             'src/coldatoms_lib/coldatoms_lib.pyx'],
    include_dirs=['./src/coldatoms_lib/', numpy.get_include()],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args
    )])

packages = find_packages(where='src',
                         exclude=('tests', 'docs', 'examples'))

setup(
    name='cold_atoms',
    version='0.0.0',
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
