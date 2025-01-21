.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

===================================
Sale Subscription TicketBai Disable
===================================

Overview
========

The **Sale Subscription TicketBai Disable** module is designed to disable the functionality for validating and sending invoices related to the TicketBai system in the **Sale Subscription** module. This is useful when you need to prevent the automatic integration with the TicketBai system for subscriptions.

Features
========

- **Disable TicketBai Integration**:

  - Disables the `validate_and_send_invoice` function in the **Sale Order** model, effectively preventing the automatic validation and sending of invoices tied to the TicketBai system.

Usage
=====

1. **Install the Module**:

   - Install the **Sale Subscription TicketBai Disable** module from the Apps menu.

2. **Effect on Sales Orders**:

   - After installing this module, the `validate_and_send_invoice` method will be disabled for sales orders created under the **Sale Subscription** module. This prevents the automatic validation and sending of invoices related to TicketBai.


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
