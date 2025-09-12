.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Barcode Format
==============

This module allows you to define custom barcode formats in Odoo 14, supporting both fixed and variable formats.

Features
========

* Format types: **Fixed** or **Variable**
* Assign a model (default: `stock.move.line`)
* Link multiple suppliers to each format (Many2many)
* View formats from supplier form (One2many)
* Support for GS1 prefixes and field positions

Usage
=====

1. Go to *Inventory > Configuration > Formats* to create a format.
2. Select type, model, and suppliers.
3. Add lines:
   - Fixed: field, start/end position
   - Variable: field and GS1 prefix
4. View related formats from the supplier form.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.
If you find a bug, please check whether it has already been reported. If not, help us by providing a detailed report.

**Do not contact contributors directly for support or help with technical issues.**

Credits
=======

Authors
~~~~~~~

* AvanzOSC

Contributors
~~~~~~~~~~~~

* Ane Gurruchaga <aneavanzosc@gmail.com>
* Ana Juaristi <anajuaristi@avanzosc.es>
