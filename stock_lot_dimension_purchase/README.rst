.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

============================
Stock Lot Dimension Purchase
============================

This module extends Odoo Purchase Management to support dimension-based quantity calculations in purchase order lines.

It integrates product dimensions and supplier-specific weight and length information into purchase orders, allowing purchase quantities to be calculated according to the product pricing method.

The module supports purchasing calculations based on weight, length, or a combination of dimensional values, while retaining the standard quantity-based purchasing workflow.

Features
--------

- Extends purchase order lines with product dimensional information:
  - Length
  - Height
  - Width
  - Dimensional unit of measure
  - Volume
  - Weight
- Automatically retrieves product dimensions and pricing method when selecting a product.
- Retrieves supplier-specific purchase weight and length information from vendor pricelists.
- Introduces a dimensional quantity field to support alternative quantity calculations.
- Supports different pricing methods:
  - Quantity
  - Weight
  - Length
  - Weight × Length
- Automatically recalculates purchase quantities based on the selected pricing method and dimensional values.
- Converts weight and length quantities into the purchase order line unit of measure when applicable.
- Automatically calculates purchase order line volume based on product dimensions.
- Displays dimensional and purchasing information directly in purchase order lines.

Data Model
----------

**purchase.order.line**

- Length (`product_length`):
  - Length associated with the purchased product.

- Height (`product_height`):
  - Height associated with the purchased product.

- Width (`product_width`):
  - Width associated with the purchased product.

- Dimensional Unit (`dimensional_uom_id`):
  - Unit of measure used for product dimensions.

- Volume (`volume`):
  - Automatically calculated volume based on product dimensions.

- Weight (`product_weight`):
  - Weight retrieved from the selected product.

- Purchase Weight (`purchase_weight`):
  - Theoretical weight per unit retrieved from the selected vendor pricelist.

- Purchase Weight Unit (`purchase_weight_uom_id`):
  - Unit of measure associated with the purchase weight.

- Purchase Length (`purchase_length`):
  - Length per unit retrieved from the selected vendor pricelist.

- Purchase Length Unit (`purchase_length_uom_id`):
  - Unit of measure associated with the purchase length.

- Pricing Method (`pricing_method`):
  - Defines the calculation method applied to the purchase quantity.

- Dimensional Quantity (`dimension_qty`):
  - Quantity used as the basis for dimensional purchase calculations.

Logic Overview
--------------

- When a product is selected in a purchase order line:
  - The pricing method is retrieved from the product.
  - Product length, height, and width are copied to the purchase line.
  - The dimensional unit of measure is retrieved.
  - The product weight is initialized.

- When a supplier pricelist is selected:
  - The purchase weight and its unit of measure are retrieved.
  - The purchase length and its unit of measure are retrieved.
  - The dimensional quantity is initialized using the supplier minimum quantity.

- Purchase quantity calculations depend on the selected pricing method:

  - **Quantity (`qty`):**
    - Uses the standard Odoo purchase quantity behavior.

  - **Weight (`weight`):**
    - Converts the supplier purchase weight into the purchase order line unit of measure.
    - Calculates the purchase quantity as:
      - `product_qty = dimension_qty × converted_purchase_weight`

  - **Length (`length`):**
    - Converts the supplier purchase length into the purchase order line unit of measure.
    - Calculates the purchase quantity as:
      - `product_qty = dimension_qty × converted_purchase_length`

  - **Weight × Length (`wl`):**
    - Calculates the purchase quantity using:
      - `product_qty = dimension_qty × product_height × purchase_length × purchase_weight`

- Purchase quantity calculations are triggered when the pricing method, dimensional quantity, purchase weight, or purchase length changes in the purchase order form.

- Purchase order line volume is calculated using:
  - `product.template._calc_volume()`

- Volume calculation depends on:
  - Length
  - Height
  - Width
  - Dimensional unit of measure

- The calculated purchase quantity is stored in the standard `product_qty` field, allowing standard Odoo purchasing processes to use the resulting quantity.

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
