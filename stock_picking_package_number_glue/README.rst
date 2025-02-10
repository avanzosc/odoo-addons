.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=================================
Stock Picking Package Number Glue
=================================

Overview
========

The **Stock Picking Package Number Glue** module extends the **Stock Picking** functionality by automatically synchronizing the `number_of_packages` field with the `packages_qty` field. This ensures that the number of packages is correctly updated whenever the quantity of packages is modified.

Features
========

- **Automatic Synchronization**:

  - Automatically updates the `number_of_packages` field based on the value of the `packages_qty` field in stock pickings.

- **Onchange Trigger**:

  - Uses the `@api.onchange` decorator to track changes in the `packages_qty` field and update the `number_of_packages` field accordingly.

Usage
=====

1. **Install the Module**:

   - Install the **Stock Picking Package Number Glue** module from the Apps menu.

2. **Modify Package Quantity**:

   - When editing a stock picking, update the `packages_qty` field.

3. **Automatic Update**:

   - The `number_of_packages` field will be automatically updated to match the value of `packages_qty`.

Configuration
=============

No additional configuration is required for this module. It works automatically once installed.

Testing
=======

Perform the following tests to ensure the module is working correctly:

- Create or edit a stock picking.

- Change the value of the `packages_qty` field.

- Verify that the `number_of_packages` field is automatically updated with the same value as `packages_qty`.

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
