.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Stock Picking Report LED
========================

This module customizes the stock picking report (`stock.report_picking`) for better readability in warehouse operations.

Description
-----------

- Groups lines by product and shows total quantity.
- Displays each lot below the product with its barcode and number.
- Removes unused columns: "To", "Product Barcode", and the top barcode.
- Replaces "Serial Number" label with "Lot/Serie".

Requirements
------------

- The `stock` module must be installed.

How to use
----------

- Install the module.
- Open a picking and print the report.

License
-------

This module is licensed under AGPL-3.

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

