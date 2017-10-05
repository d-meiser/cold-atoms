from setuptools import setup
import sys
import os


with open('README.md') as f:
    readme = f.read()


with open('LICENSE') as f:
    license = f.read()


exec(open('src/coldatoms/version.py').read())


def require_build(argv):
    """This tells us whether we need to build the package."""

    info_commands = ['--help-commands', '--name', '--version', '-V',
                        '--fullname', '--author', '--author-email',
                        '--maintainer', '--maintainer-email', '--contact',
                        '--contact-email', '--url', '--license', '--description',
                        '--long-description', '--platforms', '--classifiers',
                        '--keywords', '--provides', '--requires', '--obsoletes']
    # Add commands that do more than print info, but also don't need Cython and
    # template parsing.
    info_commands.extend(['egg_info', 'install_egg_info', 'rotate'])

    for command in info_commands:
        if command in argv[1:]:
            return False

    return True


def get_package_info():
    """Assembles info for package and external modules."""

    from Cython.Build import cythonize
    from setuptools import find_packages, Extension
    import numpy

    extra_compile_args = [
        '-DDSFMT_MEXP=19937'
        ]
    if sys.platform == 'win32':
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
    return dict(
        packages=packages,
        package_dir={'': 'src'},
        ext_modules=coldatoms_lib,
    )


def setup_package():
    metadata = dict(
        name='coldatoms',
        maintainer='Dominic Meiser',
        version=__version__,
        description='Collection of python tools for cold atoms simulations',
        long_description=readme,
        author='Dominic Meiser',
        author_email='dmeiser79@gmail.com',
        url='https://github.com/d-meiser/cold-atoms',
        license=license,
    )
    if require_build(sys.argv):
        metadata.update(get_package_info())
    setup(**metadata)



if __name__ == '__main__':
    setup_package()
