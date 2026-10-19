.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=====================================
Purchase Order Show Pickings By Group
=====================================

This module extends the default behavior of `purchase.order` to replace the standard picking shortcut button. Instead of showing only the pickings directly linked to the purchase order lines, it shows **all** ``stock.picking`` **records that share the same procurement group** (``group_id``).

Key changes:

- Adds a new ``group_picking_count`` computed field that counts all pickings sharing the same ``group_id`` as the purchase order.
- Adds a new ``action_view_group_picking`` method that opens a list of all those pickings.
- Replaces the standard picking stat button with one using ``action_view_group_picking``.

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
* Lucía Echeverría <luciaecheverria@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
