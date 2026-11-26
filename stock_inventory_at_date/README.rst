.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=======================
Stock Inventory At Date
=======================

This module allows performing physical inventory adjustments at a past date,
replicating the stock levels that existed at that point in time based on stock
move lines.

Features
--------

* Adds an **Accounting Date** field to inventory adjustments. When set to a
  past date, the inventory operates in historical mode.
* In historical mode, the **Qty at Inventory Date** column is shown with the
  stock calculated from move lines up to that date (entries minus exits), and
  the standard **On Hand Quantity** column is hidden to avoid confusion.
* The **Counted Quantity** is pre-filled automatically with the historical
  stock, so users only need to correct lines where a discrepancy is found.
* The inventory **difference** is computed as counted minus historical stock
  (not counted minus current stock), ensuring the adjustment move reflects
  the real discrepancy found at the historical date.
* The adjustment stock move and its lines are **dated at the accounting date**,
  so the correction appears at the right point in the stock history and
  accounting reports.
* Supports products with **lots, packages and owners** — the historical
  calculation is done in two SQL queries regardless of the number of lines,
  making it suitable for large inventories (5,000+ lines).
* For inventories set to today's date or a future date, the module behaves
  identically to the standard Odoo inventory adjustment.

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

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>
