.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=====================
Stock Quant Valuation
=====================

This module extends the **Stock Quant** and **Production Lot** models to
provide additional cost and valuation information for inventory quants
and lots.

Features
========

Production Lot
--------------

* **Average Price**:

  Calculates the average price of a production lot based on completed
  stock move lines entering an internal location from a non-internal
  location.

  The average price is calculated as the total amount of the relevant
  stock move lines divided by their total done quantity.

  The calculated average price is also displayed on the production lot
  form view.

Stock Quant
-----------

* **Product Cost**:

  Displays the standard cost of the product related to the quant.

* **Lot Average Unit Price**:

  Uses the average price of the linked lot when a lot is available.
  If the quant has no lot, it falls back to the product's last purchase
  price.

* **Lot Average Value**:

  Calculates the value of the quant by multiplying its quantity by the
  lot average unit price.

* **Lot Purchase Cost**:

  Uses the purchase cost of the linked lot when a lot is available.
  If the quant has no lot, it falls back to the product's last purchase
  price.

* **Lot Purchase Value**:

  Calculates the value of the quant by multiplying its quantity by the
  lot purchase cost.

* **Value**:

  Stores the standard quant value, allowing it to be aggregated when
  grouping records in the Stock Quant tree view.

The module enhances the **Inventory Adjustments** (Stock Quant tree view)
by displaying these additional cost and valuation fields for improved
inventory analysis and control.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_.

In case of trouble, please check there if your issue has already been
reported. If you spotted it first, help us improve the module by providing
detailed feedback.

Do not contact contributors directly about support or help with technical
issues.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

For specific questions regarding this module, please contact the
contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer
to the LICENSE file or visit
`GNU Affero General Public License v3
<https://opensource.org/licenses/AGPL-3.0>`_.
