.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
   :alt: License: AGPL-3

==================================
Account Move Line Product Category
==================================

Overview
========

The **Account Move Line Product Category** module adds the product category field to invoice lines, allowing users to easily view and filter by product categories in the invoice line pivot views. This provides better insight into sales and accounting data, especially when analyzing performance by product categories.

Features
========

- **Product Category Field**: Adds the product category field to invoice lines, which is automatically related to the product's category.
- **Enhanced Pivot Views**: The product category field is available in pivot views for better reporting and analysis.

Usage
=====

1. **Install the Module**:

   - Install the module via Odoo's Apps interface.

2. **Viewing Product Category on Invoice Lines**:

   - Navigate to **Accounting > Customers > Invoices**.
   - Open an invoice and view the **Product Category** field in the line items.

3. **Reporting**:

   - In the pivot view of invoice lines, you can now group or filter data by **Product Category** to analyze sales performance by category.

Configuration
=============

No additional configuration is required. The product category field is automatically populated from the related product's category.

Testing
=======

Test the following scenarios:

- **Product Category on Invoice Lines**:

  - Create an invoice with products that belong to different categories.
  - Verify that the **Product Category** field is correctly displayed and populated for each product in the invoice lines.

- **Pivot View**:

  - Go to the pivot view of invoice lines and confirm that the **Product Category** field is available for grouping and filtering data.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

For module-specific questions, please contact the contributors directly. Support requests should be made through the official channels.

License
=======

This project is licensed under the AGPL-3 License. For more details, please refer to the LICENSE file or visit <https://www.gnu.org/licenses/agpl-3.0.html>.
