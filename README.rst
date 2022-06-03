****************************
Mopidy-Radiooooo
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Radiooooo
    :target: https://pypi.org/project/Mopidy-Radiooooo/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/github/workflow/status/kaveenr/mopidy-radiooooo/CI
    :target: https://github.com/kaveenr/mopidy-radiooooo/actions
    :alt: CI build status

Stream Radiooooo on Mopidy!


Installation
============

Install by running::

    python3 -m pip install Mopidy-Radiooooo

See https://mopidy.com/ext/radiooooo/ for alternative installation methods.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Radiooooo to your Mopidy configuration file::

    [radiooooo]
    enabled = true

Development
===========

1. Install Mopidy on your system and clone this repository.

2. Set up a virtualenv.

   ``$ python -m venv env --system-site-packages``

3. Install mopidy-jellyfin to the virtualenv.

   ``$ env/bin/python setup.py develop``

4. Start development setup.

   Mopidy can be launched from the virtualenv with ``env/bin/mopidy``


Project resources
=================

- `Source code <https://github.com/kaveenr/mopidy-radiooooo>`_
- `Issue tracker <https://github.com/kaveenr/mopidy-radiooooo/issues>`_
- `Changelog <https://github.com/kaveenr/mopidy-radiooooo/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `Kaveen Rodrigo <https://github.com/kaveenr>`__
- Current maintainer: `Kaveen Rodrigo <https://github.com/kaveenr>`__
- `Contributors <https://github.com/kaveenr/mopidy-radiooooo/graphs/contributors>`_
