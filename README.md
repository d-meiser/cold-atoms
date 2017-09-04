[![Build Status](https://travis-ci.org/d-meiser/cold-atoms.svg?branch=master)](https://travis-ci.org/d-meiser/cold-atoms)
[![AppVeyor](https://img.shields.io/appveyor/ci/d-meiser/cold-atoms.svg)](https://ci.appveyor.com/project/d-meiser/cold-atoms/history)
[![Coverage Status](https://coveralls.io/repos/github/d-meiser/cold-atoms/badge.svg?branch=master)](https://coveralls.io/github/d-meiser/cold-atoms?branch=master)
[![Stories in Ready](https://badge.waffle.io/d-meiser/cold-atoms.png?label=ready&title=Ready)](https://waffle.io/d-meiser/cold-atoms)

# What is it?

The cold-atoms library is a tool box for the simulation of ensembles of neutral
atoms or ions for atomic, molecular, and optical physics (AMO) experiments. Its
design goals and principles are:

- Enable rapid and interactive experimentation and exploration. In our opinion,
  the best way of using the cold-atoms library is in a jupyter notebook. High
  performance computing workflows including massive compute jobs at large scale
  are not a primary focus.
- cold-atoms aims to be a loose collection of tools rather than an opinionated
  framework.
- Coherence and unity of the library is ensured by the consistent use numpy
  arrays as a simple representation for most kinds of data. "It is better to
  have 100 functions operate on one data structure than 10 functions on 10 data
  structures." —Alan Perlis
- When the choice is between "easy" and "simple" we choose simple. Cold atoms
  experiments and their simulation needs are much too varied for us to come up
  with easy solutions that work well for many users.

Computationally, we represent atomic ensembles as collections of point
particles with data describing their internal state. In this way, cold-atoms'
approach is similar to that of a molecular dynamics simulation or a tracking
code for the simulation of particle accelerators. Simulations requiring a fluid
representation of the particles, wave mechanics (e.g. Bose-Einstein
condensates), or a correct account of quantum statistics are beyond the scope of
the cold-atoms library.


# Getting started

Currently, the best way to obtain and use the cold-atoms library is by
downloading and building its source. We recommend installing cold-atoms and its
dependencies into a [python sandbox](https://virtualenv.pypa.io/en/stable/).
Installing into a sandbox is possible without super-user privileges and there is
no risk of breaking the system python distribution.


## Linux

```shell
# Download the package source from github.
git clone https://github.com/d-meiser/cold-atoms

cd cold-atoms

# Download external dependencies.
pip install -r requirements.txt

# Build package.
python setup.py develop

# Run the tests of the package.
nosetests

# Install the package.
pip install .

# Have a look at the examples.
cd examples
jupyter notebook &
```


## Mac

The instructions given for Linux above should work for Mac as well.


## Windows

Windows users may wish to check
out
[cold-atoms' appveyor project](https://ci.appveyor.com/project/d-meiser/cold-atoms).
Binary installers and package files can be downloaded from the artifacts of a
recent build of the master branch. The 32bit builds are currently broken and
they 64bit builds have not been tested nearly as thoroughly as the linux or
windows builds. Any help in improving the state of the windows package is
greatly appreciated.


# Contributing

If you wish to contribute to this project, please do the following:

- Fork and clone source from GitHub.
- Make sure all tests run on your system.
- Make your changes on a new branch without breaking any tests.
- Open a pull request on GitHub.

All python code should adhere to PEP8 and we use the linux kernel style guide
for C code.

To file a ticket pleas use
the [github issue tracker](https://github.com/d-meiser/cold-atoms/issues).


# License

cold-atoms is distributed under the GPLv3 license.
See [the license file](LICENSE) for details.


# Acknowledgements

The cold-atoms library relies on a number of open source libraries including

* [numpy](http://www.numpy.org/)
* [matplotlib](https://matplotlib.org/)
* [Python](http://www.python.org/)
* [jupyter](http://jupyter.org)
* [dSFMT library for random number generation](http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/SFMT/)

