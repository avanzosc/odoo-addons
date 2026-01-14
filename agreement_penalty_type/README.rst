.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

========================
Agreement Penalty Types
========================

This module links penalty types to agreements so each contract can define its own penalty settings.

**Features**

- New model `agreement.penalty.type` to connect agreements with penalty types.
- Stores number, term (days/months/years), penalty percentage, active subscription count and notes per agreement line.
- Agreement extended with a One2many of linked penalty types, shown in a dedicated tab.

**Usage**

1. Open an Agreement and add penalty types in the new tab/list.
2. Set term, percentage and other details manually for that agreement.
3. Track active subscription count and notes per penalty link.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Aner Arregi <aneravanzosc@gmail.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
