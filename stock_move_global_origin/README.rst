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
manufacturing order and stock move that serves it is automatically tagged
with the same **Global Origin** (the name of that initial sale order):

* the deliveries of the sale order, with all their picking steps;
* the purchase orders that supply it (including draft and dropshipping
  ones) and their receipts;
* the manufacturing orders that supply it, their components and
  byproducts, including subcontracting;
* the intercompany sale and purchase orders, in any company, and
  everything that supplies them in turn;
* backorders, returns and scraps of all of the above.

The origin flows from each order to whatever is bought or made for it,
so it can be ticked before or after confirming the order, even when the
chain is already done. Unticking ``Initial`` clears the Global Origin from
the whole chain again. Orders never marked as ``Initial`` are left
untouched and don't show up in the report.

Only what is linked to the sale order belongs to its chain: goods served
from stock or replenished by reordering rules are not tagged. When a
purchase or manufacturing order supplies more than one tracked sale
order, the whole document is tagged with one of them, while each sale
order keeps its own deliveries.

The Global Origin is a label, not a unique identifier: it holds the name of
the initial sale order. Sale orders share their numbering by default, but
if two initial orders end up with the same name (per-company sequences,
imports, data written through the API...), their chains show up together
in the report. Renaming an initial order renames its whole chain.

Cancelling also cuts the chain, because Odoo removes the links between the
cancelled document and the rest (so that what was running can be used for
other needs, or replaced by a new order):

* A cancelled sale order and its cancelled deliveries keep their Global
  Origin, but the purchases and manufacturing orders that were running
  for it leave the chain. Odoo leaves an exception activity on them.
* A cancelled purchase order leaves the chain itself, while the rest of
  the chain keeps its Global Origin.

If the stored values ever get out of date (for instance, data coming from
a previous version), select the sale orders and use **Action > Recompute
Global Origin** (administrators only) to compute their chains again.

How to use it
=============

Go to the **Global Origin** menu (top-level, next to Inventory) and open
**Global Report**. It shows the stock moves that belong to a tracked cycle
with the following default setup, all of which can be changed freely from
the search bar:

* **Filter**: only non-cancelled moves are shown by default. The
  *Not Cancelled* filter can be removed to include cancelled moves.
* **Grouping**: moves are grouped by Global Origin → Company →
  Operation Code (IN, OUT, MO…) → Product, both in the list and in the
  pivot view. Any grouping can be removed or reordered from the
  *Group By* menu.
* **Pivot view**: by default only *Demand* is available as a measure.
  When the rows are grouped by *Status*, each status row is coloured:
  green for done moves, red for cancelled ones and yellow for the rest.

Clicking on any row in the list opens the standard stock move form.

The report follows the usual multi-company rules: to see a whole
intercompany chain, select all its companies in the company switcher.

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
