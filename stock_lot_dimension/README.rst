.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===================
Stock Lot Dimension
===================

This module extends Odoo Product Management and Inventory to support dimensional information on products, stock lots, and vendor pricelists.

It allows users to configure product pricing methods based on quantity, weight, length, or weight multiplied by length.

The module also introduces theoretical weight and length information in vendor pricelists, allowing suppliers to define their own dimensional values and units of measure.

Additionally, it extends stock lots with dimensional fields and automatically calculates their volume based on length, height, width, and the selected dimensional unit of measure.

Features
--------

* Adds a pricing method to products, supporting:

  * Quantity
  * Weight
  * Length
  * Weight × Length

* Adds a configurable dimension display order to product categories, allowing users to choose the order in which length, height, and width are displayed.

* Extends vendor pricelists with:

  * Theoretical purchase weight and its unit of measure.
  * Theoretical purchase length and its unit of measure.

* Automatically initializes theoretical weight and length values from the selected product when configuring vendor pricelists.

* Extends stock lots with:

  * Length
  * Height
  * Width
  * Dimensional unit of measure
  * Volume
  * Weight

* Automatically calculates stock lot volume based on its dimensions.

* Restricts dimensional units of measure to the Length category and purchase weight units to the Weight category.

* Displays additional dimensional information in product forms, product lists, vendor pricelists, and stock lot forms.

Configuration
-------------

**Product Categories**

Users can configure the order in which product dimensions are displayed through the ``Dimension Order Method`` field.

Available options are:

* Length, Height, Width
* Length, Width, Height
* Width, Length, Height
* Width, Height, Length
* Height, Length, Width
* Height, Width, Length

The selected order is applied to the dimensional fields displayed in product forms.

**Products**

Users can configure the ``Pricing Method`` field on products.

Available methods are:

* **Quantity:** Pricing based on product quantity.
* **Weight:** Pricing based on product weight.
* **Length:** Pricing based on product length.
* **Weight × Length:** Pricing based on the product weight multiplied by its length.

The pricing method is intended for use by additional modules implementing dimensional purchase pricing.

**Vendor Pricelists**

Vendor pricelists include the following additional fields:

* Theoretical Weight
* Weight Unit of Measure
* Purchase Length
* Length Unit of Measure

When selecting a product, the theoretical weight and length are initialized from the corresponding product dimensions.

These values can be adjusted independently for each supplier.

Theoretical dimensions can therefore differ between the product configuration and the supplier's purchasing specifications.

**Stock Lots**

Stock lots include additional dimensional information:

* Length
* Height
* Width
* Dimensional Unit of Measure
* Volume
* Weight

Volume is automatically calculated from the lot dimensions and the selected dimensional unit of measure.

Data Model
----------

**product.category**

* Dimension Order Method (``dim_order_method``):

  * Defines the display order of length, height, and width in product forms.
  * The default order is Length, Height, Width.

**product.template**

* Pricing Method (``pricing_method``):

  * Defines the dimensional pricing method associated with the product.
  * Available options: Quantity, Weight, Length, and Weight × Length.
  * The default method is Quantity.

* Dimension Order Method (``dim_order_method``):

  * Related to ``product.category.dim_order_method``.
  * Determines the display order of product dimensions.

**product.supplierinfo**

* Theoretical Weight (``purchase_weight``):

  * Defines the theoretical weight associated with the supplier's product.

* Purchase Weight Unit (``purchase_weight_uom_id``):

  * Unit of measure used for the theoretical purchase weight.
  * Restricted to the Weight category.

* Purchase Length (``purchase_length``):

  * Defines the theoretical length associated with the supplier's product.

* Purchase Length Unit (``purchase_length_uom_id``):

  * Unit of measure used for the theoretical purchase length.
  * Restricted to the Length category.

**stock.lot**

* Length (``product_length``):

  * Length of the stock lot.

* Height (``product_height``):

  * Height of the stock lot.

* Width (``product_width``):

  * Width of the stock lot.

* Dimensional Unit (``dimensional_uom_id``):

  * Unit of measure used for length, height, and width.

* Volume (``volume``):

  * Automatically calculated volume based on the stock lot dimensions.

* Weight (``product_weight``):

  * Weight associated with the stock lot.

Logic Overview
--------------

**Product Pricing Configuration**

Product pricing methods are configured through ``product.template.pricing_method``.

The available pricing methods are Quantity, Weight, Length, and Weight × Length.

This module provides the pricing method configuration but does not modify purchase order amount calculations.

**Dimension Display Order**

The order in which product dimensions appear is configured through ``product.category.dim_order_method``.

This configuration is inherited by products through the related field ``product.template.dim_order_method``.

**Vendor Dimensional Information**

When selecting a product in a vendor pricelist:

* ``purchase_weight`` is initialized from the product weight.
* ``purchase_length`` is initialized from the product length.

Supplier-specific theoretical dimensions can subsequently be modified independently of the product.

**Stock Lot Volume Calculation**

Stock lot volume is calculated using:

``product.template._calc_volume()``

The calculation depends on:

* Length
* Height
* Width
* Dimensional unit of measure

The volume is automatically recomputed when any of these values change.

**Integration with Purchasing**

This module provides the product pricing methods and supplier-specific theoretical dimensions required for dimensional purchasing.

Purchase order line calculations, dimensional quantities, and purchase amounts are handled by the separate ``stock_lot_dimension_purchase`` module.

This separation allows dimensional product and stock lot information to be managed independently of dimensional purchasing functionality.

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
