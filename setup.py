#!/usr/bin/env python

import setuptools
from distutils.core import setup, Extension
import versioneer
import numpy as np
import os
from Cython.Build import cythonize

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def c_ext():
    return [Extension('skxray.ext.ctrans', ['src/ctrans.c'],
                      define_macros=[('USE_THREADS', None)])]


def cython_ext():
    """Walk through the directory tree and find cython files to compile

    Returns
    -------
    list
        List of compiled cython extensions
    """
    cython_extensions = []
    eca = ['-Wno-unused-function', '-Wno-unreachable-code']
    for parent, folders, files in os.walk('skxray'):
        for f in files:
            if f.endswith('.pyx'):
                # skxray/core/accumulators -> skxray.core.accumulators.histogram
                parent_name = parent.replace('/', '.') + '.' + \
                              os.path.splitext(f)[0]
                ext_name = os.path.join(parent, f)
                print(parent_name, ext_name)
                e = Extension(parent_name, [ext_name],
                              extra_compile_args=eca)
                # cython_extensions.append(*cythonize(ext_name))
                cython_extensions += cythonize(e)
    return cython_extensions

setup(
    name='scikit-xray',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Brookhaven National Lab',
    description="Data analysis tools for X-ray science",
    packages=setuptools.find_packages(exclude=['doc']),
    include_dirs=[np.get_include()],
    package_data={'skxray.core.constants': ['data/*.dat']},
    install_requires=['six', 'numpy'],  # essential deps only
    ext_modules=c_ext() + cython_ext(),
    url='http://github.com/scikit-xray/scikit-xray',
    keywords='Xray Analysis',
    license='BSD',
    classifiers=['Development Status :: 3 - Alpha',
                 "License :: OSI Approved :: BSD License",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.4",
                 "Topic :: Scientific/Engineering :: Physics",
                 "Topic :: Scientific/Engineering :: Chemistry",
                 "Topic :: Software Development :: Libraries",
                 "Intended Audience :: Science/Research",
                 "Intended Audience :: Developers",
                 ],
    )
