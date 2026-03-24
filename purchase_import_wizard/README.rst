.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Purchase Import Wizard
======================

Module to import Purchase Orders from Excel files, improving usability and automation in purchase operations.

* Allows importing purchase orders and lines from structured Excel files.
* Automatically validates suppliers, products, warehouses, and picking types.
* Creates purchase orders and order lines from imported data.
* Provides log of errors and highlights issues in import lines.
* Button box for quick access to imported lines and created purchase orders.

Key Features
============
- Wizard to upload Excel files and import purchase orders.
- Validation of imported lines, with error reporting in **Error Log**.
- Automatic creation of **Purchase Orders** and **Order Lines** from import lines.
- Quick access buttons for **Import Lines** and **Purchase Orders**.
- Statusbar and state management for import workflow (`draft`, `2validate`, `pass`, `error`, `done`).

Configuration
=============
1. Go to **Purchases → Configuration → Import Purchase Orders**.
2. Upload an Excel file using the column names in the **Help** tab.
3. Click **Validate** to check lines and **Process** to create purchase orders.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please check there if your issue has already been reported. If you spotted it first, help us improve it by providing detailed feedback.

Credits
=======

Contributors
------------

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
