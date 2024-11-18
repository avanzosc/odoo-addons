.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=============================
Stock Inventory Import Wizard
=============================

Overview
========

The **Stock Inventory Import Wizard** module allows users to import inventory data directly into Odoo. It simplifies the process of creating inventory records by providing a wizard to import inventory lines and generate stock quant movements automatically. This module links imported data to inventory records, stock locations, and products, offering an efficient way to handle large-scale inventory imports.

Features
========

- Imports inventory data including products, locations, and quantities from a file into Odoo.

- Automatically creates inventory records and lines from imported data.

- Validates and processes inventory lines, including actions like creating quants and stock moves.

- Tracks the import process with error handling and logging.

- Allows users to associate the import with a specific company.

Usage
=====

1. **Install the Module**:

   - Install the **Stock Inventory Import Wizard** module from the Apps menu.

2. **Import Inventory Data**:

   - Navigate to the **Inventory** app and find the **Stock Inventory Import** wizard.

   - Upload the file containing inventory data, including details like products, locations, lots, and quantities.

3. **Process the Import**:

   - Review the import lines, validate the data, and create stock moves and quants for each line.

   - The wizard will automatically handle the creation of inventory records based on the imported data.

4. **Viewing the Data**:

   - Once processed, the wizard allows users to view the inventory, inventory lines, and related stock move lines.

5. **Create Quants**:

   - The wizard provides an option to create stock quants for the imported inventory lines, adjusting the stock levels as necessary.

Configuration
=============

Ensure that the **Stock Inventory Import Wizard** module is installed and correctly configured with the necessary permissions for users to access the inventory data and import functionality.

Testing
=======

Test the following scenarios to ensure the module functions as expected:

- **Test Inventory Import**:

  - Upload a file with inventory data and verify that inventory records are correctly created.
  
- **Test Data Validation**:

  - Ensure that missing or incorrect data in the import file is logged and flagged for correction.
  
- **Test Quants Creation**:

  - Verify that stock quants are correctly created for imported inventory lines.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
