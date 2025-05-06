.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

======================================================
Account Move Invoice Date Due Normal Date in Tree View
======================================================

Overview
========

The **Account Move Invoice Date Due Normal Date in Tree View** module modifies the behavior of the **Invoice Date Due** field in the tree view of account moves. It enhances the visibility and functionality of the field based on the payment state of the invoice.

Features
========

- **Dynamic Visibility**:

  - Hides the **Invoice Date Due** field for invoices with certain payment states, such as "Paid", "In Payment", or "Reversed".
  
- **Optional Field**:

  - Adds the **Invoice Date Due** field as an optional field in the tree view for better customization.

Usage
=====

1. **Install the Module**:

   - Install the **Account Move Invoice Date Due Normal Date in Tree View** module from the Apps menu.

2. **View the Changes**:

   - Navigate to the **Invoices** list view in the **Accounting** app.

   - Observe that the **Invoice Date Due** field is hidden for invoices with specific payment states ("Paid", "In Payment", or "Reversed").

   - The field is available as an optional column for other invoices.

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
