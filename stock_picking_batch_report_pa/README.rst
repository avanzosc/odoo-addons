.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=============================
Stock Picking Batch Report PA
=============================

This module adds a PDF report for `stock.picking.batch` that groups picking moves by customer and date.

**Features**

- Report grouped by customer and date within each picking batch.
- Shows move line details: description, containers, lots, quantity, UoM, and origin document.
- Displays totals per batch (boxes, pallets, kg, cardboard boxes).

**Technical**

- Report action: `action_report_picking_batch_pa`
- Model: `stock.picking.batch`
- QWeb template: `stock_picking_batch_report_pa.report_grouped_picking_pa`

**Usage**

Open a picking batch and print the **Grouped Picking Report PA** to get a detailed grouped delivery report.

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
