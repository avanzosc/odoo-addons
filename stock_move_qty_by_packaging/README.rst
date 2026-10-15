.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===========================
Stock move qty by packaging
===========================

Overview
========

The **Stock Packaging Quantity** module enhances stock operations by adding packaging information and packaging quantities to stock moves and stock move lines.

It allows users to select a product packaging directly from detailed stock operations, specify the number of packages handled, and automatically calculate the corresponding product quantity.

The module also integrates packaging information coming from sales order lines and displays packaging quantities for both demanded and completed quantities in delivery operations.

Features
========

- **Packaging on Stock Move Lines**:

    - Adds the `product_packaging_id` field to `stock.move.line`.

    - Only packaging options associated with the selected product can be chosen.

    - Adds the `product_packaging_qty` field to specify the number of packages handled.

- **Automatic Quantity Calculation**:

    - When a packaging is selected, the packaging quantity is automatically initialized to `1`.

    - The `qty_done` value is automatically updated using the quantity defined on the selected product packaging.

    - When the packaging quantity changes, the completed product quantity is recalculated using:

\`Packaging Quantity × Packaging Unit Quantity\`

- **Packaging Quantity on Stock Moves**:

    - Adds the `product_packaging_qty` field to `stock.move`.

    - The packaging quantity is calculated from the packaging quantities entered on the associated stock move lines.

    - If no move lines are available and the stock move originates from a sales order line, the packaging quantity is obtained from the sales order line.

- **Demand Packaging Quantity**:

    - Adds the `demand_product_packaging_qty` field to stock moves.

    - Calculates the expected number of packages according to the stock move demand and the packaging quantity defined on the related sales order line.

- **Done Packaging Quantity**:

    - Adds the `done_product_packaging_qty` field to stock moves.

    - Calculates the completed number of packages proportionally according to the quantity already processed.

- **Sales Order Packaging Integration**:

    - When a stock move originates from a sales order line containing packaging information, the corresponding packaging and packaging quantity are propagated to the stock operation.

    - This keeps the packaging information consistent between sales orders and delivery operations.

- **Detailed Operations Integration**:

    - Adds the `Packaging` and `Packaging Quantity` fields to the detailed stock operation views.

    - Packaging information can be modified while the operation is active.

    - The fields become read-only when the stock operation is cancelled or completed.

- **Delivery Operation Integration**:

    - Adds packaging quantities to the stock picking operations tree.

    - Displays the packaging quantity associated with each stock move.

    - Optionally displays both demanded and completed packaging quantities for users with the Stock Packaging feature enabled.

Usage
=====

1. **Install the Module**:

    - Install the **Stock Packaging Quantity** module via the Apps menu.

2. **Configure Product Packaging**:

    - Navigate to a product and configure the available packaging options.

    - Define the quantity of product units contained in each packaging.

3. **Use Packaging in Stock Operations**:

    - Open a delivery order or another stock operation.

    - Access the detailed operations.

    - Select a value in the `Packaging` field.

    - Enter the required number of packages in `Packaging Quantity`.

    - The completed product quantity will be calculated automatically according to the selected packaging.

4. **Packaging from Sales Orders**:

    - When the stock operation originates from a sales order line with packaging information, the module uses that information to calculate the packaging quantities associated with the stock move.

5. **Review Packaging Quantities**:

    - In the delivery order operations, review the packaging quantity associated with each stock move.

    - Users with the Stock Packaging feature enabled can also display the demanded and completed packaging quantities.

Configuration
=============

No additional module-specific configuration is required.

Product packaging must be configured on the corresponding products in order to use the packaging fields.

The optional demand and completed packaging quantity fields are available to users belonging to the standard Odoo **Stock Packaging** group.

Testing
=======

Test the following to ensure the module works as intended:

- Verify that the `Packaging` field only displays packaging options associated with the selected product.

- Verify that selecting a packaging automatically sets `Packaging Quantity` to `1`.

- Verify that selecting a packaging updates `qty_done` with the quantity configured on the packaging.

- Verify that changing `Packaging Quantity` recalculates `qty_done` correctly.

- Verify that removing the selected packaging resets the packaging quantity and completed quantity correctly.

- Verify that `product_packaging_qty` on the stock move is calculated from the associated stock move lines.

- Verify that packaging information is obtained from the sales order line when applicable.

- Verify that `demand_product_packaging_qty` correctly represents the packaging quantity corresponding to the demanded stock quantity.

- Verify that `done_product_packaging_qty` correctly represents the packaging quantity corresponding to the completed stock quantity.

- Verify that packaging information is propagated to detailed operation lines when forcing detailed operations as done.

- Verify that the packaging fields are visible in both stock move line operation views.

- Verify that packaging fields become read-only when the stock operation is in `done` or `cancel` state.

- Verify that the packaging quantity, demand packaging quantity, and completed packaging quantity are displayed correctly in the delivery order operations.

Configuration
=============

No additional module-specific configuration is required.

Product packaging must be configured on the corresponding products in order to use the packaging fields.

The optional demand and completed packaging quantity fields are available to users belonging to the standard Odoo **Stock Packaging** group.

Testing
=======

Test the following to ensure the module works as intended:

- Verify that the `Packaging` field only displays packaging options associated with the selected product.

- Verify that selecting a packaging automatically sets `Packaging Quantity` to `1`.

- Verify that selecting a packaging updates `qty_done` with the quantity configured on the packaging.

- Verify that changing `Packaging Quantity` recalculates `qty_done` correctly.

- Verify that removing the selected packaging resets the packaging quantity and completed quantity correctly.

- Verify that `product_packaging_qty` on the stock move is calculated from the associated stock move lines.

- Verify that packaging information is obtained from the sales order line when applicable.

- Verify that `demand_product_packaging_qty` correctly represents the packaging quantity corresponding to the demanded stock quantity.

- Verify that `done_product_packaging_qty` correctly represents the packaging quantity corresponding to the completed stock quantity.

- Verify that packaging information is propagated to detailed operation lines when forcing detailed operations as done.

- Verify that the packaging fields are visible in both stock move line operation views.

- Verify that packaging fields become read-only when the stock operation is in `done` or `cancel` state.

- Verify that the packaging quantity, demand packaging quantity, and completed packaging quantity are displayed correctly in the delivery order operations.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
