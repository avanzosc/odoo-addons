.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===============================
Stock Inventory Date Lot Filter
===============================

This  module extends the stock inventory functionality by allowing users to filter the generated inventory lines using two new fields:

- **Create Date Before**: Only include stock quants created before a specified date.
- **Lot Contains**: Only include stock quants with lot names containing a specific substring.

**Features**

- Adds two new fields to the inventory form:
  - `Create Date Before` (Datetime)
  - `Lot Contains` (Char)
- Filters the inventory lines generated during the inventory adjustment according to these fields.
- Fully integrated with the inventory adjustment form view.
  
**Technical Details**

**New Fields**

- `create_date_before` (Datetime): Filters out any stock quant created after this date.
- `lot_contains` (Char): Filters out any lot whose name does not contain this substring (case-insensitive).

**Method Override**

Overrides `_get_inventory_lines_values()` in `stock.inventory` to apply the custom filters.

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
