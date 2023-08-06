package-manifest
----------------

|pipeline| |coverage|

|pypiVersion| |doi0.3.0|


A Python 3 framework for creating and maintaining a generalised manifest of files
inspired by the Python MANIFEST.in. The framework could be used as the basis of a
packaging tool to define the files needed for distribution of the package.

.. contents::

.. section-numbering::


Main Features
=============

* YAML based file format
* Manifest include & exclude actions using Unix globs, ``**`` (recursive) and ``*``


Installation
============

The simplest way to acquire ``package_manifest`` is using ``pip``.

.. code-block:: bash

   pip install package-manifest


Getting Started
===============

The manifest YAML file is simply a list of the include and exclude actions to
comprise the formulation of a list of files. Each include/exclude action can take
multiple Unix-style globs per the
`Python standard library <https://docs.python.org/3/library/glob.html?highlight=glob#glob.glob>`_.

.. code-block:: yaml

   ---
   # Python MANIFEST.in is used as a reference:
   # https://docs.python.org/3.6/distutils/sourcedist.html
   #
   manifest:
     # include the files ./LICENSE and ./README.md
     - include:
         - LICENSE
         - README.md
     # exclude ./*.orig files
     - exclude:
       # NOTE: have to be careful to quote values starting with a wildcard (*) because
       #       it has special meaning in YAML syntax.
       - "*.orig"
     # include *.h & *.c files anywhere in the ./include directory and its subdirectories.
     - include:
       - include/**/*.h
       - include/**/*.c
     # exclude all files and subdirectories in the ./temp directory.
     - exclude:
       - temp/**/*
     # include files called "Makefile" anywhere in the tree.
     - include:
       - "**/Makefile"
     # exclude files matching *.txt, *.tmp, test anywhere in the tree.
     - exclude:
       - "**/*.txt"
       - "**/*.tmp"
       - "**/test"
     # remove the ./bin directory and all files and subdirectories.
     - exclude:
       - bin/**/*
     # add the ./src directory and all files and subdirectories.
     - include:
       - src/**/*

Using the manifest file is simply a matter of importing the library and using the
``from_file`` class method to import the operations and apply them to the
specified root directory of the directory tree from which to extract files.

.. code-block:: python

   from package_manifest import Manifest

   this_manifest = Manifest.from_file( "manifest.yml" )
   manifest_files = this_manifest.apply(".")

``manifest_files`` now contains a Python set of the file names from the current working
directory ``'.'`` and its subdirectories that have been filtered by the
sequential include and exclude actions specified in the file ``manifest.yml``.


DOI Archive
===========

+-------+------------+
| 0.2.0 | |doi0.2.0| |
+-------+------------+
| 0.3.0 | |doi0.3.0| |
+-------+------------+


.. |pipeline| image:: https://gitlab.com/blueskyjunkie/package-manifest/badges/master/pipeline.svg
   :target: https://gitlab.com/blueskyjunkie/package-manifest/commits/master
   :alt: pipeline status

.. |coverage| image:: https://gitlab.com/blueskyjunkie/package-manifest/badges/master/coverage.svg
   :target: https://gitlab.com/blueskyjunkie/package-manifest/commits/master
   :alt: coverage report

.. |pypiVersion| image:: https://badge.fury.io/py/packageManifest.svg
   :target: https://badge.fury.io/py/packageManifest
   :alt: PyPI Version

.. |doi0.2.0| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1165137.svg
   :target: https://doi.org/10.5281/zenodo.1165137
   :alt: DOI v0.2.0

.. |doi0.3.0| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1165942.svg
   :target: https://doi.org/10.5281/zenodo.1165942
   :alt: DOI v0.3.0
