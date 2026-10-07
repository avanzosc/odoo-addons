.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=======================
Stock B2B Availability
=======================

This module adds a B2B-only available quantity to products, computed from a
subset of stock locations flagged as "for B2B stock control".

A product's regular ``qty_available`` mixes every warehouse/location. This
module lets you mark specific stock locations as B2B stock, and exposes a
``b2b_virtual_available`` quantity that only considers those locations:
on-hand quantity in the flagged locations, minus quantity already committed
to outgoing deliveries to customers from those same locations.

Key features
============

* **For B2B stock control** checkbox on stock locations (list and form
  views), to flag which locations count as B2B stock.
* **B2B Quantity** (``b2b_virtual_available``) computed field on
  ``product.product``: on-hand quantity in flagged locations minus quantity
  already committed to customer deliveries from those locations.

Usage / How to test
====================

1. Go to **Inventory → Configuration → Locations**, open a location and
   check **For B2B stock control** (or toggle it from the locations list).
2. On any product with stock in that location, the **B2B Quantity** field
   reflects only that subset of the stock.

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
