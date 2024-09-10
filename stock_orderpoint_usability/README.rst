.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Stock ordepoint usability
=========================

Overview
========

The **Stock Warehouse Orderpoint Customization** module extends the stock warehouse orderpoint functionality in Odoo by adding additional fields and buttons to the tree and form views. It allows users to track more detailed information about products, suppliers, and reorder points.

Features
========

- **Additional Fields**:
  
  - `qty_available`, `incoming_qty`, `outgoing_qty`, `consumed_last_twelve_months`, and `months_with_stock` are added to the **Orderpoint** model to show product-related metrics.
  - `supplier_pending_to_receive` field is added to track pending quantities from suppliers.

- **Recompute Button**:
  
  - A "Recompute Qty to Order" button is available in both the tree and form views to manually trigger recalculation of quantities.

- **View Enhancements**:
  
  - Both the **tree** and **form** views are modified to show the new fields and buttons, improving the usability of stock management.

Bug Tracker
===========


Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>


Do not contact contributors directly about support or help with technical issues.
