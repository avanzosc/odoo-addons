.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=======================
Stock Picking No Origin
=======================

This module extends the `stock.picking` model to help identify pickings whose **origin** does not match any existing **Sales Order** or **Purchase Order**.

**Features**

- Adds a computed Boolean field `origin_not_exists` on `stock.picking`.
- The field is `True` if the `origin` value does not correspond to any existing Sales Order or Purchase Order.
- Adds a new filter in the internal transfer view to easily find such pickings.

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
* Lucía Echeverría <luciaavanzosc@gmail.com>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
