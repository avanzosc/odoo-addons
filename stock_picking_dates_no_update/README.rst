.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: License: LGPL-3

=============================
Stock Picking Dates No Update
=============================

Overview
========

The **Stock Picking Dates No Update** module overrides the default behavior in Odoo related to the **`date_done`** and **`scheduled_date`** fields in the `stock.picking` model. The module prevents automatic modification of these fields when validating a stock picking, ensuring the dates remain unchanged after validation.

Features
========

- Prevents automatic update of the **`date_done`** field in the `stock.picking` model when the picking is validated.
- Prevents automatic update of the **`scheduled_date`** field in the `stock.picking` model when the picking is validated.
- Keeps the **`date_done`** and **`scheduled_date`** fields as they were before validation, preserving the original values.

Usage
=====

1. Go to **Inventory → Operations → Transfers**.
2. Select a **Transfer** and validate it.
3. After the validation, the **`date_done`** and **`scheduled_date`** fields will not be modified automatically by the system.
4. These fields will remain as they were before the validation.

Configuration
=============

No additional configuration is required.

Testing
=======

1. Create a **Transfer** and set the **`scheduled_date`** and **`date_done`** values.
2. Validate the **Transfer**.
3. After validation, check that the **`scheduled_date`** and **`date_done`** fields retain their original values, without being automatically updated.

Bug Tracker
===========

Bugs and issues can be reported on the GitHub repository:
`GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For further information, please contact the contributors.

License
=======

This project is licensed under the LGPL-3 License.
For more details, see the LICENSE file or visit:
<https://www.gnu.org/licenses/lgpl-3.0.html>.
