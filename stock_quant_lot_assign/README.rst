.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

======================
Stock Quant Lot Assign
======================

This module allows assigning lots or serial numbers to the stock quants that
have no lot, for products that were not tracked and are now tracked by lots or
by serial numbers.

When a product starts being tracked by lots, its existing stock remains in
quants without lot. This module adds an *Assign Lot* action to the stock
quants that creates a new lot for each selected quant and moves its quantity
to that lot through an inventory adjustment, so stock moves, traceability and
valuation remain consistent.

Features
--------

* Adds an *Assign Lot* action to the stock quant lists.
* For products tracked by lots, creates one new lot per processed quant, with
  its whole quantity.
* For products tracked by serial numbers, creates one new serial number and one
  quant per unit. For example, a quant of 3 units creates 3 quants of 1 unit,
  each with its own serial number.
* Names the lots and serial numbers with a configurable prefix and a sequential
  number (for example, ``BORRAR000001``).
* Moves the quantity of the quant without lot to the new quants, in the same
  location, package and owner, through inventory adjustment moves.
* Unreserves the quantities reserved in the processed quants and reserves the
  affected moves again after the assignment.
* Adds the *Assigned Lot Prefix* setting, ``BORRAR`` by default.

Configuration
-------------

Go to *Inventory > Configuration > Settings*. In the *Traceability* section,
with *Lots & Serial Numbers* enabled, set the *Assigned Lot Prefix*.

The default prefix is ``BORRAR``, so the created lots can be easily found and
renamed with their real names later.

Usage
-----

#. Set the product tracking to *By Lots* or *By Unique Serial Number*.
#. Go to *Inventory > Operations > Physical Inventory* and filter the quants
   of the product without lot.
#. Select the quants and click *Actions > Assign Lot*.
#. The list of the new quants with their lots is opened.

Only inventory administrators (``stock.group_stock_manager``) can use the
action.

Logic Overview
--------------

**Processed Quants**

Only the selected quants that meet all these conditions are processed:

* The product is tracked by lots or by serial numbers.
* The quant has no lot.
* The quant has a positive quantity.
* The location is internal or transit.

If none of the selected quants meets them, an error is raised.

For products tracked by serial numbers, the quantity of the quant must be a
whole number of units. Otherwise, an error lists the wrong quants and nothing
is processed.

**Reservations**

If any processed quant has reserved quantities, the moves that reserve them
are unreserved with ``_do_unreserve()`` before the assignment. After the
assignment, those moves are reserved again with ``_action_assign()``, so they
reserve the new lots or serial numbers, or any other available stock,
according to the removal strategy.

Odoo does not unreserve operations already marked as picked. If a quant is
still reserved after unreserving, an error lists it and nothing is processed.
Unpick or process those operations first.

**Lot Assignment**

For each processed quant:

#. New lots are created for the product and company of the quant: one lot for
   products tracked by lots, or one serial number per unit for products tracked
   by serial numbers. Their names are the configured prefix followed by the
   next number of the ``stock.quant.lot.assign`` sequence. If a lot with that
   name already exists for the product, the next number is used.
#. A quant is created in inventory mode for each new lot, with the same
   location, package and owner. Its counted quantity is the whole quantity of
   the original quant for lots, or 1 for serial numbers.
#. The counted quantity of the original quant is set to zero.

Then the inventory of all of them is applied at once with
``_apply_inventory()``. Odoo creates and validates two inventory adjustment
moves with the reference *Lot assignment*:

* One from the location to the inventory adjustment location, without lot, for
  each original quant.
* One from the inventory adjustment location to the location for each new lot
  or serial number.

Odoo allows inventory adjustment moves of tracked products without lot, so the
product tracking is not modified during the process.

**Valuation**

With automated valuation, both moves are valued at the product cost. With
standard or average cost, the stock value does not change. With FIFO, the
value can change slightly depending on the cost layers.

Known Issues / Roadmap
----------------------

* Lots are created with a generic name. Rename them with their real names
  from *Inventory > Products > Lots/Serial Numbers*.

Technical Information
---------------------

**Dependencies**

* ``stock``

**Extended Models**

* ``res.config.settings``
* ``stock.quant``

**Data**

* ``data/ir_config_parameter.xml``: ``stock_quant_lot_assign.lot_prefix``
  system parameter, ``BORRAR`` by default (``noupdate``).
* ``data/ir_sequence.xml``: ``stock.quant.lot.assign`` sequence for the lot
  names (``noupdate``).
* ``data/ir_actions_server.xml``: *Assign Lot* server action, bound to the
  stock quant lists.

**Main Methods**

* ``stock.quant.action_assign_lot()``
* ``stock.quant._get_quants_to_assign_lot()``
* ``stock.quant._check_assign_lot_serial_quantities()``
* ``stock.quant._unreserve_assign_lot_quants()``
* ``stock.quant._get_assign_lot_quantities()``
* ``stock.quant._prepare_assign_lot_vals()``
* ``stock.quant._prepare_assign_lot_quant_vals()``

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
* Berezi Amubieta Eceiza <bereziamubieta@avanzosc.es>

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
