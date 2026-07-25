.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

============================
Stock Lot Dimension Purchase
============================

This module extends Odoo Purchase Management to support dimensional pricing in purchase order lines.

It integrates product dimensions and supplier-specific theoretical weight and length information into purchase orders, allowing purchase amounts to be calculated according to the product pricing method.

The module supports purchasing calculations based on quantity, weight, length, or weight multiplied by length, while preserving the standard purchase quantity for inventory operations.

Features
--------

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

Data Model
----------

**purchase.order.line**

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

* Dimensional Quantity (``dimension_qty``):

  * Computed and stored dimensional pricing factor.
  * Automatically calculated based on the pricing method and editable weight and length values.

Logic Overview
--------------

**Product and Supplier Information**

When a product is selected in a purchase order line:

* The pricing method is retrieved from the product.
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

Technical Information
---------------------

**Dependencies**

* ``stock_lot_dimension``

**Extended Models**

* ``purchase.order.line``

**Main Methods**

* ``_compute_dimension_qty()``
* ``onchange_product_id()``
* ``_compute_amount()``
* ``_prepare_base_line_for_taxes_computation()``
* ``_prepare_account_move_line()``

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
