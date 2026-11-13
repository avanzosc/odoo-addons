.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===================
Stock Lot Dimension
===================

This module extends Odoo Inventory and Product Management to support dimensional information on stock lots, products, and vendor pricelists.

It allows users to define product pricing methods based on quantity, weight, length, or weight multiplied by length. It also introduces theoretical weight and length information in vendor pricelists, enabling supplier-specific dimensional data.

Additionally, the module extends stock lots with dimensional fields and automatically calculates their volume based on length, height, width, and the selected dimensional unit of measure.

Features
--------

- Adds a pricing method to products, supporting:
  - Quantity
  - Weight
  - Length
  - Weight × Length
- Extends vendor pricelists with:
  - Theoretical purchase weight and its unit of measure.
  - Purchase length and its unit of measure.
- Automatically initializes vendor weight and length values from the selected product.
- Adds dimensional information to stock lots:
  - Length
  - Height
  - Width
  - Dimensional unit of measure
  - Volume
  - Weight
- Automatically calculates stock lot volume based on its dimensions.
- Supports dimensional units of measure from the Length category.
- Displays the additional fields in product forms, vendor pricelists, and stock lot forms.

Data Model
----------

**product.template**

- Pricing Method (`pricing_method`):
  - Defines the calculation method associated with the product.
  - Available options: Quantity, Weight, Length, and Weight × Length.

**product.supplierinfo**

- Theoretical Weight (`purchase_weight`):
  - Defines the theoretical purchase weight associated with the supplier's product.

- Purchase Weight Unit (`purchase_weight_uom_id`):
  - Unit of measure used for the theoretical purchase weight.

- Purchase Length (`purchase_length`):
  - Defines the purchase length associated with the supplier's product.

- Purchase Length Unit (`purchase_length_uom_id`):
  - Unit of measure used for the purchase length.

**stock.lot**

- Length (`product_length`):
  - Length of the stock lot.

- Height (`product_height`):
  - Height of the stock lot.

- Width (`product_width`):
  - Width of the stock lot.

- Dimensional Unit (`dimensional_uom_id`):
  - Unit of measure used for length, height, and width.

- Volume (`volume`):
  - Automatically calculated volume based on the stock lot dimensions.

- Weight (`product_weight`):
  - Weight associated with the stock lot.

Logic Overview
--------------

- Product pricing methods are configured through:
  - `product.template.pricing_method`

- Vendor dimensional information is initialized when selecting a product:
  - `purchase_weight` is populated from the product weight.
  - `purchase_length` is populated from the product length.

- Stock lot volume is calculated using:
  - `product.template._calc_volume()`

- Volume calculation depends on:
  - Length
  - Height
  - Width
  - Dimensional unit of measure

- The volume is automatically recomputed when any of these values change.

- Dimensional units of measure are restricted to the Length category.

- The module provides dimensional information for inventory and purchasing processes without modifying standard stock movement behavior.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us fix it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Berezi Amubieta <bereziamubieta@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
