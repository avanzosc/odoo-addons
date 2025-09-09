.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Stock Lot Expiration Date Input
===============================

This module improves usability in stock operations with lots/serial numbers
by allowing users to manually input an expiration date in detailed operations.

* Adds a new field **Manual Expiration Date** on stock move lines.
* When confirming operations, this date is copied to the related lot/serial number.
* Visibility of the field depends on product and picking type configuration.

Key Features
============
- New field **Manual Expiration Date** on Stock Move Lines.
- Field only visible if:
  
  * The picking type has **"Create New Lots/Serial Numbers"** enabled.
  * The product has **"Use Expiration Date"** enabled.

- When assigning a lot/serial number, the **manual expiration date** is saved into the lot.

Configuration
=============
1. Go to **Inventory → Configuration → Products** and enable **Tracking by Lots/Serials** and **Expiration Date** for a product.
2. Go to **Inventory → Configuration → Operation Types** and enable **Create New Lots/Serial Numbers**.
3. On stock transfers (detailed operations), you will now see the **Manual Expiration Date** field.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Ane Gurruchaga <aneavanzosc@gmail.com>

Do not contact contributors directly about support or help with technical issues.
