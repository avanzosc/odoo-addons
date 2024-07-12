.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Stock Automatic Lot Name Creation
=================================

Overview
========

The Stock Automatic Lot Name Creation module enhances the functionality of stock move lines in Odoo by automatically assigning lot names under specific conditions.

Features
========

- Automatically assigns lot names to stock move lines based on certain criteria.
- Conditions checked:
  - If the picking type requires lot creation (`create_lots` is enabled).
  - If the product is traceable (`product.product.tracking` is set to 'lot').
  - If the lot name field (`lot_name`) is empty, it assigns a lot name based on the picking name and origin.


Usage
=====

Once installed, the module will automatically handle the assignment of lot names to stock move lines based on the configured conditions.

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
* Unai Beristain <unaiberistain@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
