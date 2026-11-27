.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===================
Stock Lot Dimension
===================

This module extends Odoo Product Management and Inventory to manage dimensional
information on products, stock lots and stock quants.

It allows users to configure a pricing method based on quantity, weight,
length, or weight multiplied by length. The pricing method is defined on the
product category and inherited by its products, which can override it
individually. Product categories also define the order in which length, height
and width are displayed.

Stock lots display the dimensions, volume and weight of their product, each one
next to its unit of measure (for example, ``Width: 3 mm`` or ``Weight: 2.5 kg``).
The same information is displayed as columns in the stock quant list.

Dimensions and weights are managed with 8 decimal places, using specific
decimal precisions that do not affect the rest of Odoo quantities.

Features
--------

* Adds a pricing method to product categories and products, supporting:

  * Quantity
  * Weight
  * Length
  * Weight × Length

* Products take the pricing method of their category by default, and it can
  be changed on a specific product.

* Changing the pricing method of a category updates all the products of that
  category.

* Adds a configurable dimension display order to product categories, which
  defines the order in which length, height and width are displayed in product
  forms.

* Extends stock lots with the following information, taken from the lot
  product:

  * Pricing method.
  * Length, height and width, with the product dimensional unit of measure.
  * Volume, with the volume unit of measure.
  * Weight, with the weight unit of measure.

* Displays every lot value and its unit of measure on the same line in the
  stock lot form.

* Extends stock quants with the same product information as stock lots, and
  displays it as optional columns in the editable stock quant list.

* Adds two decimal precisions, ``Product Dimension`` and
  ``Product Dimension Weight``, with 8 decimal places, used by the length,
  height, width and weight fields of products, stock lots and stock quants.
  They are also used by ``stock_lot_dimension_purchase``.

* Displays additional dimensional information in product forms, product lists,
  stock lot forms and stock quant lists.

Configuration
-------------

**Product Categories**

Go to *Inventory > Configuration > Product Categories*. The *Logistics* section
contains the following fields.

``Dimension Order Method``, with the following options:

* Length, Height, Width (default)
* Length, Width, Height
* Width, Length, Height
* Width, Height, Length
* Height, Length, Width
* Height, Width, Length

The selected order is applied to the dimensional fields displayed in the
product forms of that category.

``Pricing Method``, with the following options:

* **Quantity:** Pricing based on product quantity (default).
* **Weight:** Pricing based on product weight.
* **Length:** Pricing based on product length.
* **Weight × Length:** Pricing based on the product weight multiplied by its
  length.

This is the default pricing method of the products of the category.

**Products**

The ``Pricing Method`` field of the product form is filled in automatically
with the pricing method of the product category, both when the product is
created and when its category is changed.

It can be changed on a specific product to set a different pricing method.

.. warning::

   Changing the pricing method of a category overwrites the pricing method of
   **all** the products of that category, including the products whose pricing
   method was changed manually. Set the specific pricing methods again after
   changing the category.

The pricing method is intended to be used by additional modules implementing
dimensional purchase pricing, such as ``stock_lot_dimension_purchase``.

Length, height, width and their unit of measure are configured on the product
through the ``product_dimension`` module. Weight and volume are the standard
Odoo product fields.

**Weight and Volume Units of Measure**

In standard Odoo, product weight and volume are always expressed in the units
of measure defined by system parameters:

* Weight: kilograms by default, or pounds when ``product.weight_in_lbs`` is
  set to ``1``.
* Volume: cubic meters by default, or cubic feet when
  ``product.volume_in_cubic_feet`` is set to ``1``.

These settings can be changed in *Inventory > Configuration > Settings*.

**Decimal Precision**

The module creates the following decimal precisions, both with 8 decimal
places:

* ``Product Dimension``: length, height and width of products, stock lots and
  stock quants.
* ``Product Dimension Weight``: weight of products, stock lots and stock
  quants.

``stock_lot_dimension_purchase`` uses the same precisions for vendor
pricelists, purchase order lines and the purchase information of stock lots.

They can be changed in *Settings > Technical > Database Structure > Decimal
Accuracy* (developer mode). They are created with ``noupdate="1"``, so module
updates do not overwrite the configured values.

The standard ``Product Unit of Measure`` and ``Stock Weight`` precisions are not
modified, so other Odoo quantities and weights keep their configuration.

Usage
-----

**Stock Lots**

Open a lot in *Inventory > Products > Lots/Serial Numbers*. The *Product
Dimensions* section displays:

* Pricing Method of the product.
* Length, Height and Width, followed by the dimensional unit of measure.
* Volume, followed by the volume unit of measure.
* Weight, followed by the weight unit of measure.

These values are read-only in the lot. To change them, edit the product.

**Stock Quants**

Open *Inventory > Reporting > Stock*. The list displays the following optional
columns after the unit of measure:

* Pricing Method (hidden by default).
* Length, Height, Width and Dim. UoM.
* Volume and Vol. UoM.
* Weight and Weight UoM.

Columns can be shown or hidden from the optional columns menu of the list.
These values are read-only. To change them, edit the product.

Data Model
----------

**product.category**

* Dimension Order Method (``dim_order_method``):

  * Defines the display order of length, height and width in product forms.
  * The default order is Length, Height, Width.

* Pricing Method (``pricing_method``):

  * Default dimensional pricing method of the products of the category.
  * Available options: Quantity, Weight, Length and Weight × Length.
  * The default method is Quantity.

**product.template**

* Pricing Method (``pricing_method``):

  * Dimensional pricing method associated with the product.
  * Stored, editable computed field depending on
    ``categ_id.pricing_method``.
  * Same options as the category field.

* Dimension Order Method (``dim_order_method``):

  * Related to ``categ_id.dim_order_method`` and stored.
  * Determines the display order of product dimensions.

* Length, Height, Width (``product_length``, ``product_height``,
  ``product_width``) and Weight (``weight``):

  * Redefined in ``product.template`` and ``product.product`` only to change
    their decimal precision (``Product Dimension`` and
    ``Product Dimension Weight``).

**stock.lot**

All the fields are related to the lot product (``product_id``) and read-only.

* Pricing Method (``pricing_method``):

  * Related to ``product_id.pricing_method``. Stored.

* Length (``product_length``):

  * Related to ``product_id.product_length``. Stored.

* Height (``product_height``):

  * Related to ``product_id.product_height``. Stored.

* Width (``product_width``):

  * Related to ``product_id.product_width``. Stored.

* Dimensional UoM (``product_dimensional_uom_id``):

  * Related to ``product_id.dimensional_uom_id``. Stored.
  * Unit of measure of length, height and width.

* Volume (``product_volume``):

  * Related to ``product_id.volume``. Stored.

* Volume UoM (``product_volume_uom_name``):

  * Related to ``product_id.volume_uom_name``. Not stored.
  * Label of the volume unit of measure (for example, ``m³``).

* Weight (``product_weight``):

  * Related to ``product_id.weight``. Stored.

* Weight UoM (``product_weight_uom_name``):

  * Related to ``product_id.weight_uom_name``. Not stored.
  * Label of the weight unit of measure (for example, ``kg``).

Length, height and width use the ``Product Dimension`` decimal precision, and
weight uses ``Product Dimension Weight``.

**stock.quant**

Same fields as ``stock.lot``, with the same names, related to the quant
product (``product_id``) and read-only:

* ``pricing_method``, ``product_length``, ``product_height``,
  ``product_width``, ``product_dimensional_uom_id``, ``product_volume`` and
  ``product_weight``: stored.
* ``product_volume_uom_name`` and ``product_weight_uom_name``: not stored.

Logic Overview
--------------

**Product Pricing Configuration**

The default pricing method is configured on the product category through
``product.category.pricing_method``.

``product.template.pricing_method`` is a stored, editable computed field
(``readonly=False``) computed by ``_compute_pricing_method()``:

* When a product is created, or its category is changed, it takes the pricing
  method of the category.
* The user can then set a different value on the product, which is kept.
* When the pricing method of a category is changed, Odoo recomputes the field
  for all the products of that category, overwriting the manual values.

Stock lots and purchase order lines read the pricing method of the product, so
they use the specific value of the product when one has been set.

This module provides the pricing method configuration but does not modify
purchase order amount calculations.

**Dimension Display Order**

The order in which product dimensions appear is configured through
``product.category.dim_order_method``.

Products inherit this configuration through the related field
``product.template.dim_order_method``, which is used in the product form views
to show length, height and width in the selected order.

**Stock Lot Dimensions**

Stock lot dimensions, volume and weight are not entered on the lot. They are
related to the lot product and are updated automatically when the product
changes.

The dimensional unit of measure is a ``uom.uom`` record defined on each product
by the ``product_dimension`` module.

Weight and volume units of measure are the labels provided by standard Odoo
(``weight_uom_name`` and ``volume_uom_name``). As product weight and volume are
always stored in the units defined by the system parameters, the value and the
unit displayed in the lot always match. These labels are not stored, so they
are updated when the system parameters change.

**Stock Quant Dimensions**

Stock quants use the same approach as stock lots. Their fields are related to
the quant product, not to the lot, so they are also available for quants of
products that are not tracked by lots.

The values are stored so that the stock quant list can be sorted, filtered and
grouped by them.

**Integration with Purchasing**

This module provides the product pricing methods and the decimal precisions
required for dimensional purchasing. It does not depend on the Purchase app.

Vendor pricelist theoretical dimensions, purchase order line calculations,
dimensional quantities, purchase amounts and the purchase information of stock
lots are handled by the separate ``stock_lot_dimension_purchase`` module.

Known Issues / Roadmap
----------------------

* The dimension display order of the product category is applied to product
  forms but not to the stock lot form or the stock quant list, where dimensions
  are always displayed as Length, Height, Width.
* Lot and quant dimensions are always the product dimensions. Lot-specific
  dimensions are not supported.
* Values saved before installing or updating to the 8 decimal precisions keep
  the decimals they were saved with.

Technical Information
---------------------

**Dependencies**

* ``stock``
* ``product_dimension``

**Extended Models**

* ``product.category``
* ``product.template``
* ``product.product``
* ``stock.lot``
* ``stock.quant``

**Data**

* ``data/decimal_precision.xml``: ``Product Dimension`` and
  ``Product Dimension Weight`` decimal precisions.

**Inherited Views**

* ``stock.view_production_lot_form``
* ``stock.view_stock_quant_tree_editable``
* ``product_dimension.product_normal_form_view``
* ``product_dimension.product_template_only_form_view``
* ``product.product_product_tree_view``
* ``product.product_template_tree_view``
* ``product.product_category_form_view``

**Main Methods**

* ``product.template._compute_pricing_method()``

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
