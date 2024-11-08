.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

==============
Custom Reports
==============

Overview
========

The **Custom Reports** module customizes the layout of Odoo's default templates for key business documents, including invoices, purchase orders, and delivery slips. This module provides a foundation for additional branding and layout adjustments to better match the organization’s requirements.

Features
========

- **Customizable Document Templates**:

  - **Invoice Template**: Adds customizations to the invoice template (`account.report_invoice_document`).

  - **Purchase Order Template**: Adds customizations to the purchase order template (`purchase.report_purchaseorder_document`).

  - **Delivery Document Template**: Adds customizations to the delivery slip template (`stock.report_delivery_document`).

Usage
=====

1. **Install the Module**:

   - Go to the Apps menu and install the **Custom Reports** module.

2. **Print Customized Documents**:

   - Print invoices, purchase orders, and delivery slips to see the additional custom text in each document's layout.

Configuration
=============

No additional configuration is required for this module. The customizations are automatically added to the specified document templates upon installation.

Testing
=======

Test the following scenarios to ensure the module functions as expected:

- **Invoice Document**:

  - Print an invoice and confirm that the customizations appear in the layout.
  
- **Purchase Order Document**:

  - Print a purchase order and verify that the customizations are included.
  
- **Delivery Document**:

  - Print a delivery slip and check for the customizations in the layout.

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

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https
