.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
Stock Lot Report Aditional 
==========================

This module duplicates the original stock lot label report (`stock.report_lot_label`) and modifies it.

Description
-----------

- The report is copied into a new module called `stock_lot_report_aditional`.
- The QWeb report is changed to show the lot number as a QR code and next to the QR code, the last five characters are displayed in plain text.
- It works exactly like the original report but with the QR code added.

Requirements
------------

- The `stock` module must be installed.

How to use
----------

- Install this module.
- Go to Inventory → Products → Lots/Serial Numbers.
- Open a lot and print the label with the QR code.

License
-------

This module is licensed under AGPL-3. See http://www.gnu.org/licenses/agpl-3.0-standalone.html.

Bug Tracker
-----------

Report bugs at https://github.com/avanzosc/odoo-addons/issues.

Credits
-------

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Ane Gurruchaga <aneavanzosc@gmail.com>

Please do not contact contributors directly for support or technical help.

