.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Barcode Format
==============

This module allows you to define custom barcode formats in Odoo 14, supporting both fixed and variable formats.

Features
========

* Define barcode formats by type: **Fixed** or **Variable**
* Assign a model (default: `stock.move.line`)
* Filter by partner (customer/vendor)
* Support for GS1 prefixes and field positions
* Field separator configurable for variable barcodes

Usage
=====

1. Go to the menu and create a new barcode format.
2. Select the format type (`fixed` or `variable`).
3. Add lines to the format:
   * For fixed: set `field`, `start position`, and `end position`.
   * For variable: set `field` and `GS1 prefix`.
4. (Optional) For variable types, you can specify a separator character.

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
