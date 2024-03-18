======================
 Access settings menu
======================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

* Open menu ``[[ Settings ]] >> Users & Companies >> Users``
* Open user form view (click on the line with the user)
* Click ``[Edit]``
* Select ``[Show Settings Menu]`` and click ``[Save]``

Usage
=====

Without this module installed:

* Non-admin user can't see the ``[[ Settings ]]`` menu.


With this module installed:

* If non-admin user has the ``[Show Settings Menu]`` right he can see the ``[[ Settings ]]`` menu.

Uninstallation
==============

After uninstalling, you need to update ``base`` module to return restriction to ``Settings`` menu back.
