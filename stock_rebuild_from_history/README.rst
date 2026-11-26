.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

==========================
Stock Rebuild From History
==========================

This module adds a server action and a cron job to enable inventory tracking on products
(``is_storable = True``) and rebuild their stock quants from historical move line data.

In Odoo 18, all physical goods share ``type = 'consu'``. The distinction between consumable
and storable is controlled by the ``is_storable`` flag. This module targets products where
``is_storable = False`` and activates inventory tracking on them, bypassing the ORM restriction
via direct SQL for products that already have stock history.

Features
--------

- Enables inventory tracking (``is_storable``) on consumable products, even if they already
  have done stock moves.
- Resets the quantities of existing quants for the product and its variants.
- Recomputes stock levels by replaying all ``done`` move lines.
- Updates or creates quants for each combination of:

  - Source & destination locations
  - Lot/serial
  - Package
  - Owner

- Rebuilds stock data accurately without deleting any quant records.

Usage
-----

**Server action (manual):**
Select one or more products in the product list, then launch *Convert Stockable and Rebuild Stock*
from the Action menu. Only products with ``is_storable = False`` are processed.

**Cron job (bulk):**
A scheduled job (*Rebuild Stock All Products*) is included but disabled by default. When enabled,
it processes all consumable products in batches and commits after each one.

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



