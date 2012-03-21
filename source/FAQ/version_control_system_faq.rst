.. _FAQ_vcs:

============================
Version Control System - FAQ
============================

.. contents::

.. _version_control_pyNEURON:

How can I use version control for compilation of nmod-files?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As the compilation of nmod-files is a binary it is not recommended to include
these within a repository. Also they can be different on varying computer
systems.

Therefore ignore these binary files. E.g. for `mercurial` add within the
.hgignore-file something like ``NEURON/i686`` (depending on your structure of
directories)

IMPORTANT: Changes of nmod-files have to be compiled on each system by hand!
