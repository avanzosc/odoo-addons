.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

==========================
Stock Import Existing Lots
==========================

This module changes how the "Import Lots" button behaves on the detailed
operations of a stock move.

In standard Odoo, both the "Generate Serial Numbers" and "Import Lots"
buttons are only shown when the move's operation type has "Create New
Lots/Serial Numbers" enabled, and importing a lot/serial name that doesn't
exist yet always creates it.

With this module:

* The "Import Lots" button is always available, regardless of whether the
  operation type allows creating new lots/serial numbers. The "Generate
  Serial Numbers" button keeps the standard behavior and only shows up when
  new lots/serial numbers can be created.
* When the operation type does **not** allow creating new lots/serial
  numbers, importing lots searches for each entered name in the existing
  lots/serial numbers of the product instead of creating it. If any of the
  entered names doesn't match an existing lot/serial number, the import is
  cancelled and a warning lists the names that were not found.
* When the operation type does allow creating new lots/serial numbers, the
  import keeps working exactly as in standard Odoo.



Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.



