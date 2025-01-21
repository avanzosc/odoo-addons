.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

==============================================================
Stock Report Delivery Document Lot ID
==============================================================

Overview
========

The **Stock Report Delivery Document Lot ID** module enhances the **Delivery Document Report** by adding the ability to display lot or serial numbers for stock moves. This provides more detailed traceability for your delivery operations.

Features
========

- **Display Lot/Serial Numbers**:

  - Adds a new column to the **Delivery Document Report** to show the lot or serial number of stock moves.
  
- **Barcode Support**:

  - Displays barcodes for the lot/serial numbers, improving operational efficiency.

- **Dynamic Visibility**:

  - Automatically shows the column only when lot or serial numbers are present in the stock move lines.

Usage
=====

1. **Install the Module**:

   - Install the **Stock Report Delivery Document Lot ID** module via the Apps menu.

2. **Check Delivery Documents**:

   - Open any delivery document and verify the presence of the `Lot/Serial Number` column.

3. **Barcodes for Lot/Serial Numbers**:

   - Confirm that barcodes for lot or serial numbers appear in the new column.

Configuration
=============

No additional configuration is needed. The module works out of the box once installed.

Testing
=======

Perform the following tests to ensure the module is working correctly:

- Verify that the `Lot/Serial Number` column appears in the **Delivery Document Report** only when there are lot or serial numbers.

- Confirm that the barcodes are correctly generated and displayed in the column.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>

* Unai Beristain <unaiberistain@avanzosc.es>

For specific questions or support, please contact the contributors.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
