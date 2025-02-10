.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

========================================================
Delivery Package Number Report
========================================================

Overview
========

The **Delivery Package Number Report** module enhances the existing **Stock Report Delivery Document** view by adding a new field to display the number of packages in the report. This is useful for tracking and reporting the number of packages associated with delivery moves.

Features
========

- **Add Number of Packages**:
  - Modifies the `stock.report_delivery_document` view to include a field showing the number of packages associated with a stock move line.
  
- **Integration with Delivery Package Number**:
  - Leverages the **Delivery Package Number** module for the `number_of_packages` field.
  
Usage
=====

1. **Install the Module**:
   - Install the **Delivery Package Number Report** module via the Apps menu.

2. **View the Report**:
   - Navigate to the stock report view for delivery documents.
   - The new `Number of Packages` field will be visible in the report.

3. **Use Case**:
   - This module is particularly useful for organizations that need to track the number of packages involved in their stock moves, especially when dealing with deliveries.

Configuration
=============

No specific configuration is required for this module. It will automatically modify the `stock.report_delivery_document` view to include the new `number_of_packages` field.

Testing
=======

Test the following to ensure the module works as intended:

- Verify that the `number_of_packages` field appears correctly in the stock delivery document report.
- Ensure the field reflects the correct data from the **Delivery Package Number** module.

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
