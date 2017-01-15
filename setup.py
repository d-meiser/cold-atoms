from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cold-atoms',
    version='0.0.0',
    description='Collection of python tools for cold atoms simulations',
    long_description=readme,
    author='Dominic Meiser',
    author_email='dmeiser79@gmail.com',
    url='https://github.com/d-meiser/cold-atoms',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
