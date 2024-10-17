.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=====================================
Website Payment Acquirer Bank Account
=====================================

Overview
========

The **Account Payment Mode and Acquirer** module integrates payment modes with bank accounts in sales. It allows users to select a bank account for payments directly from the sales order, enhancing the payment processing workflow.

Features
========

- **Bank Account Selection**: Users can select a bank account for payments directly from the sales order.
  
- **Automatic Payment Mode Assignment**: When confirming an order, the payment mode is automatically set based on the selected bank account.

- **Bank Account Management**: Users can create new bank accounts linked to partners seamlessly.

Usage
=====

1. **Install the Module**:

   - Install the module via Odoo's Apps interface.

2. **Using Bank Accounts**:

   - When creating or editing a sales order, select a bank account from the dropdown.
   - Confirm the order, and the payment mode will automatically be assigned based on the selected bank account.

Configuration
=============

No additional configuration is required. The module is ready to use once installed.

Testing
=======

Test the following scenarios:

- **Bank Account Selection**:

  - Create or edit a sales order and select a bank account.
  - Confirm the order and verify that the payment mode is set correctly.

- **Bank Account Creation**:

  - Create a new bank account from the sales order and ensure it links correctly to the partner.

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

This project is licensed under the LGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
