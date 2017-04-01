from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

coldatoms_lib = cythonize([Extension(
    'coldatoms_lib',
    sources=['src/coldatoms_lib/forces.c',
             'src/coldatoms_lib/coldatoms_lib.pyx'],
    include_dirs=['./src/coldatoms_lib/']
    )])

setup(
    name='cold-atoms',
    version='0.0.0',
    description='Collection of python tools for cold atoms simulations',
    long_description=readme,
    author='Dominic Meiser',
    author_email='dmeiser79@gmail.com',
    url='https://github.com/d-meiser/cold-atoms',
    license=license,
    packages=find_packages(where='src',
                           exclude=('tests', 'docs', 'examples')),
    package_dir={'': 'src'},
    ext_modules=coldatoms_lib
)
