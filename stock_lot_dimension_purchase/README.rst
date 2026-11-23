.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

============================
Stock Lot Dimension Purchase
============================

This module extends Odoo Purchase Management to support dimensional pricing in purchase order lines.

It integrates product dimensions and supplier-specific theoretical weight and length information into purchase orders, allowing purchase amounts to be calculated according to the product pricing method.

Vendor pricelists are extended with theoretical weight and length values and their units of measure, so each supplier can define its own purchasing specifications.

The module supports purchasing calculations based on quantity, weight, length, or weight multiplied by length, while preserving the standard purchase quantity for inventory operations.

When a lot is created on the reception of a purchase order, the dimensional information of the purchase order line is copied to the lot, so it remains available as informative data of the lot. The stock quants of that lot display the same information in the stock quant list.

Features
--------

* Extends vendor pricelists with:

  * Theoretical purchase weight and its unit of measure.
  * Theoretical purchase length and its unit of measure.

* Initializes the theoretical weight and length of vendor pricelists from the selected product.
* Restricts the units of measure of vendor pricelists to the Weight and Length categories respectively.
* Extends purchase order lines with weight and length information.
* Automatically retrieves product weight, length, and pricing method when selecting a product.
* Retrieves supplier-specific theoretical weight, length, and their units of measure from vendor pricelists.
* Allows users to manually modify weight and length values in purchase order lines.
* Introduces a computed dimensional quantity field (``dimension_qty``).
* Supports the following pricing methods:

  * Quantity
  * Weight
  * Length
  * Weight × Length

* Automatically recalculates the dimensional quantity when the pricing method, weight, or length changes.
* Calculates purchase order line amounts using the dimensional quantity, purchase quantity, and unit price.
* Preserves the standard purchase quantity (``product_qty``) for inventory operations.
* Adjusts the unit price when preparing vendor bill lines to account for dimensional pricing.
* Displays dimensional and purchasing information directly in purchase order lines.
* Copies the purchase dimensional information to the lots created on reception:

  * Pricing method.
  * Theoretical length and weight of the vendor pricelist.
  * Length and weight of the purchase order line.
  * Length and weight units of measure.

* Displays the purchase dimensional information in a *Purchase Dimensions* section of the stock lot form, as read-only values next to their units of measure.
* Displays the length of the purchase order line, with its unit of measure, in the operations of the receipt form.
* Extends stock quants with the purchase dimensional information of their lot, and displays it as optional columns in the editable stock quant list.
* Uses 8 decimal places for all lengths, weights and dimensional quantities, through the ``Product Dimension`` and ``Product Dimension Weight`` decimal precisions defined in ``stock_lot_dimension``.

Data Model
----------

**product.supplierinfo**

* Theoretical Weight (``purchase_weight``):

  * Theoretical weight per unit of the supplier's product.
  * Decimal precision: ``Product Dimension Weight``.

* Purchase Weight Unit (``purchase_weight_uom_id``):

  * Unit of measure of the theoretical purchase weight.
  * Restricted to the Weight category.
  * Defaults to the weight unit of measure defined by the system parameters.

* Purchase Length (``purchase_length``):

  * Theoretical length per unit of the supplier's product.
  * Decimal precision: ``Product Dimension``.

* Purchase Length Unit (``purchase_length_uom_id``):

  * Unit of measure of the theoretical purchase length.
  * Restricted to the Length category.
  * Defaults to millimeters.

**purchase.order.line**

Lengths (``product_length``, ``purchase_length``) and the dimensional quantity (``dimension_qty``) use the ``Product Dimension`` decimal precision. Weights (``product_weight``, ``purchase_weight``) use ``Product Dimension Weight``.

* Length (``product_length``):

  * Editable length associated with the purchased product.
  * Initialized from the product or supplier information when available.

* Weight (``product_weight``):

  * Editable weight associated with the purchased product.
  * Initialized from the product or supplier information when available.

* Purchase Weight (``purchase_weight``):

  * Theoretical weight per unit retrieved from the selected vendor pricelist.
  * Read-only in purchase order lines.

* Purchase Weight Unit (``purchase_weight_uom_id``):

  * Unit of measure associated with the theoretical purchase weight.
  * Read-only in purchase order lines.

* Purchase Length (``purchase_length``):

  * Theoretical length per unit retrieved from the selected vendor pricelist.
  * Read-only in purchase order lines.

* Purchase Length Unit (``purchase_length_uom_id``):

  * Unit of measure associated with the theoretical purchase length.
  * Read-only in purchase order lines.

* Pricing Method (``pricing_method``):

  * Defines the dimensional pricing method applied to the purchase order line.
  * Available options: Quantity, Weight, Length, and Weight × Length.
  * Uses the same options as ``stock_lot_dimension`` (``PRICING_METHOD_SELECTION``).

* Dimensional Quantity (``dimension_qty``):

  * Computed and stored dimensional pricing factor.
  * Automatically calculated based on the pricing method and editable weight and length values.

**stock.lot**

Lengths use the ``Product Dimension`` decimal precision, and weights use ``Product Dimension Weight``.

All the fields are read-only. They are filled in when the lot is created on the reception of a purchase order and cannot be changed manually.

* Purchase Pricing Method (``purchase_pricing_method``):

  * Copied from ``purchase.order.line.pricing_method``.

* Purchase Theoretical Length (``theoretical_length``):

  * Copied from ``purchase.order.line.purchase_length``.
  * Theoretical length per unit of the vendor pricelist.

* Purchase Theoretical Weight (``theoretical_weight``):

  * Copied from ``purchase.order.line.purchase_weight``.
  * Theoretical weight per unit of the vendor pricelist.

* Purchase Length (``purchase_length``):

  * Copied from ``purchase.order.line.product_length``.
  * Length used in the purchase order line.

* Purchase Length UoM (``purchase_length_uom_id``):

  * Copied from ``purchase.order.line.purchase_length_uom_id``.
  * Unit of measure of both the theoretical and the purchase length.

* Purchase Weight (``purchase_weight``):

  * Copied from ``purchase.order.line.product_weight``.
  * Weight used in the purchase order line.

* Purchase Weight UoM (``purchase_weight_uom_id``):

  * Copied from ``purchase.order.line.purchase_weight_uom_id``.
  * Unit of measure of both the theoretical and the purchase weight.

**stock.move**

* Purchase Length (``purchase_length``):

  * Related to ``purchase_line_id.product_length``. Not stored.
  * Decimal precision: ``Product Dimension``.

* Purchase Length UoM (``purchase_length_uom_id``):

  * Related to ``purchase_line_id.purchase_length_uom_id``. Not stored.

**stock.quant**

Same fields as the purchase information of ``stock.lot``, with the same names, related to the quant lot (``lot_id``), stored and read-only:

* ``purchase_pricing_method``
* ``theoretical_length`` and ``theoretical_weight``
* ``purchase_length`` and ``purchase_length_uom_id``
* ``purchase_weight`` and ``purchase_weight_uom_id``

Quants without lot, or whose lot was not created on a purchase reception, have these fields empty.

Logic Overview
--------------

**Vendor Dimensional Information**

When a product or product template is selected in a vendor pricelist:

* ``purchase_weight`` is initialized from the product weight.
* ``purchase_length`` is initialized from the product length.

The supplier's theoretical dimensions can then be modified independently of the product.

**Product and Supplier Information**

When a product is selected in a purchase order line:

* The pricing method is retrieved from the product (which takes it from its category by default, see ``stock_lot_dimension``).
* Product weight and length are initialized from the product configuration.
* The corresponding weight and length units of measure are initialized.
* If a matching vendor pricelist is found, the theoretical weight, length, and their units of measure are retrieved.
* Supplier-specific theoretical dimensions are used to initialize the editable weight and length values when they are nonzero.

The theoretical supplier dimensions remain available in separate read-only fields.

**Dimensional Quantity Calculation**

The dimensional quantity is calculated according to the selected pricing method.

* **Quantity (``qty``):**

  * ``dimension_qty = 1``

* **Weight (``weight``):**

  * ``dimension_qty = product_weight``

* **Length (``length``):**

  * ``dimension_qty = product_length``

* **Weight × Length (``wl``):**

  * ``dimension_qty = product_weight * product_length``

The dimensional quantity is automatically recomputed when the pricing method, product weight, or product length changes.

**Purchase Amount Calculation**

For quantity-based pricing, Odoo's standard purchase amount calculation is preserved.

For dimensional pricing methods, the purchase subtotal before discounts and taxes is calculated using:

::

    Subtotal = product_qty * dimension_qty * price_unit

Discounts and applicable taxes are handled through Odoo's standard tax computation mechanism.

The standard purchase quantity (``product_qty``) is not modified by dimensional pricing.

**Example**

A product is purchased with the following values:

* Purchase Quantity: 10 units
* Pricing Method: Weight
* Weight per Unit: 2 kg
* Supplier Unit Price: 3 EUR/kg

The dimensional quantity is:

::

    dimension_qty = 2

The purchase subtotal is:

::

    Subtotal = 10 * 2 * 3
    Subtotal = 60 EUR

If the user manually changes the weight per unit to 2.5 kg, the dimensional quantity and subtotal are automatically recalculated:

::

    dimension_qty = 2.5
    Subtotal = 10 * 2.5 * 3
    Subtotal = 75 EUR

**Vendor Bill Preparation**

When preparing vendor bill lines from purchase order lines, the dimensional quantity is applied to the unit price.

For dimensional pricing methods:

::

    Invoice Unit Price = Purchase Unit Price * dimension_qty

The standard purchase quantity is preserved when preparing the vendor bill.

This allows vendor bills generated from purchase orders to use an effective unit price based on the dimensional information.

**Inventory Integration**

Dimensional pricing does not modify the standard purchase quantity.

The ``product_qty`` field continues to represent the physical quantity purchased.

The module does not modify stock movement quantities or implement dimensional inventory valuation.

Additional stock valuation adaptations may be required when using automatic inventory valuation to ensure that inventory costs reflect dimensional purchase prices.

**Stock Lot Purchase Information**

The purchase dimensional information is copied to the lot when the lot is created, through ``stock.move.line._prepare_new_lot_vals()``.

This happens when a reception of a purchase order is validated and a new lot name is entered in the detailed operations. The purchase order line is obtained from ``move_id.purchase_line_id``.

The values are copied, not related, so the lot keeps the information of the purchase that originated it:

* If the purchase order line is modified after the reception, the lot is not updated.
* If an existing lot is selected in the reception, it is not modified.
* If the same lot is received several times, it keeps the information of the first reception, which created it.
* Lots created manually, or from operations other than purchase receptions, have no purchase dimensional information.

**Receipt Purchase Length**

The length of the purchase order line is displayed in the receipt moves through related fields on ``stock.move`` (``purchase_line_id.product_length``). It is not copied, so it always shows the current value of the purchase order line.

**Stock Quant Purchase Information**

The purchase dimensional information of stock quants is related to the quant lot (``lot_id``), not to the purchase order line. Every quant of a lot, in any location, displays the information of the purchase that created the lot.

The values are stored so that the stock quant list can be sorted, filtered and grouped by them.

Usage
-----

**Vendor Pricelists**

In the *Purchase* tab of the product form, set the theoretical weight and length of each vendor and their units of measure. When the product is selected, they are initialized from the product weight and length.

**Purchases and Lots**

#. Create a purchase order for a product tracked by lots and set the weight and length of the lines.
#. Confirm the order and open the reception. The *Operations* tab shows the *Length* and *Length UoM* columns of each purchase order line.
#. Enter a new lot name in the detailed operations and validate the reception.
#. Open the lot in *Inventory > Products > Lots/Serial Numbers*. The *Purchase Dimensions* section shows the information of the purchase order line.

**Stock Quants**

Open *Inventory > Reporting > Stock*. After the product dimension columns of ``stock_lot_dimension``, the list displays the following optional columns:

* Purch. Pricing Method, Theor. Length and Theor. Weight (hidden by default).
* Purch. Length and Purch. Length UoM.
* Purch. Weight and Purch. Weight UoM.

These columns are only available to users with the *Lots & Serial Numbers* setting enabled (``stock.group_production_lot``), as the information comes from the lot.

Technical Information
---------------------

**Dependencies**

* ``purchase_stock``
* ``stock_lot_dimension``

**Extended Models**

* ``product.supplierinfo``
* ``purchase.order.line``
* ``stock.lot``
* ``stock.move``
* ``stock.move.line``
* ``stock.quant``

**Inherited Views**

* ``product.product_supplierinfo_form_view``
* ``purchase.product_supplierinfo_tree_view2``
* ``purchase.purchase_order_form``
* ``stock.view_picking_form``
* ``stock_lot_dimension.view_production_lot_form``
* ``stock_lot_dimension.view_stock_quant_tree_editable``

**Main Methods**

* ``product.supplierinfo.onchange_product_id()``
* ``purchase.order.line._compute_dimension_qty()``
* ``purchase.order.line.onchange_product_id()``
* ``purchase.order.line._compute_amount()``
* ``purchase.order.line._prepare_base_line_for_taxes_computation()``
* ``purchase.order.line._prepare_account_move_line()``
* ``stock.move.line._prepare_new_lot_vals()``

**Upgrade Notes**

The vendor pricelist fields (``purchase_weight``, ``purchase_weight_uom_id``, ``purchase_length`` and ``purchase_length_uom_id``) and their views were previously defined in ``stock_lot_dimension``.

When upgrading a database where ``stock_lot_dimension_purchase`` is installed, update ``stock_lot_dimension``::

    odoo -u stock_lot_dimension

Odoo also updates the installed modules that depend on it, so both modules are updated in the same run and the stored values are kept.

``stock_lot_dimension_purchase`` must be installed before the update. Otherwise, the fields and their database columns are removed from vendor pricelists.

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
