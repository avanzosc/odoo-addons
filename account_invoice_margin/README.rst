.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

===========================================
Account Invoice Margin
===========================================

Overview
========

The **Account Invoice Margin** module adds margin calculation fields to invoice lines and invoice totals. It allows businesses to track and analyze the margin on individual invoice lines and the overall invoice margin, as well as the margin percentage.

Features
========

- **Margin Fields on Invoice Lines**: Adds fields for calculating product cost, subtotal cost, margin, and margin percentage on invoice lines.
  
- **Margin Calculation on Invoice**: Computes the total margin, total subtotal cost, and average margin percentage at the invoice level.

Usage
=====

1. **Install the Module**:
 
   - Install the **Account Invoice Margin** module via the Apps menu.

2. **View Margin Information**:
  
   - On the **Invoice Line** form, you will see the calculated fields for **Product Cost**, **Subtotal Cost**, **Margin**, and **Margin Percent**.
  
   - The **Invoice Form** will display the **Total Subtotal Cost**, **Total Margin**, and **Average Margin Percent**.

3. **Analyze Invoice Margins**:
 
   - Use the **Invoice Pivot** view to analyze the total margin, subtotal cost, and average margin percentage for invoices.

Configuration
=============

No additional configuration is required. Simply install the module to start using the margin calculation features.

Testing
=======

Test the following scenarios to ensure the module functions as expected:

- **Test Margin Calculation**:
  
  - Create an invoice and check that the **Subtotal Cost**, **Margin**, and **Margin Percent** are calculated correctly for each invoice line.

- **Test Total and Average Margin**:
  
  - Verify that the **Total Subtotal Cost**, **Total Margin**, and **Average Margin Percent** are correctly calculated at the invoice level.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
