.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

========================
Stock Move Global Origin
========================

This module lets you trace a full sale → purchase → manufacturing →
intercompany cycle as a single unit, from the first sale order to the
last delivery, no matter how many orders and moves are chained together
in between.

How it works
============

On a sale order, tick the ``Initial`` checkbox to mark it as the start of
a cycle you want to track. From that point on, every purchase order,
manufacturing order and stock move generated along the chain (including
intercompany sales/purchases) is automatically tagged with the same
**Global Origin** (the name of that initial sale order). Orders never
marked as ``Initial`` are left untouched and don't show up in the report.

Unticking ``Initial`` clears the Global Origin from the whole chain again.

How to use it
=============

Go to the **Global Origin** menu (top-level, next to Inventory) and open
**Global Report**. It shows the stock moves that belong to a tracked cycle
with the following default setup, all of which can be changed freely from
the search bar:

* **Filter**: only non-cancelled moves are shown by default. The
  *Not Cancelled* filter can be removed to include cancelled moves.
* **List view**: moves are grouped by Global Origin → Company →
  Operation Type (sequence code) → Product. Any grouping can be removed
  or reordered from the *Group By* menu.
* **Pivot view**: starts empty so you can build the analysis you need.
  By default only *Demand* is available as a measure.

Clicking on any row in the list opens the standard stock move form.

This report is also available to users without Inventory access (via the
**Global Origin Viewer** permission group), so sales or customer service
can check where an order stands without needing full Inventory permissions.
Those users only see moves that belong to a tracked cycle and have
read-only access.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
