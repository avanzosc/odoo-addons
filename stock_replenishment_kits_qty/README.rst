.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=================================
Stock Replenishment Kits Quantity
=================================

Overview
========

The **Stock Replenishment Kits Quantity** module enhances the stock replenishment process by showing the quantity of products included in kits directly within the stock orderpoint form. This allows for better inventory management and planning.

Features
========

- **Quantity in Kits Field**: Displays the total quantity of products included in kits on the stock replenishment orderpoint form.
- **Calculate and Assign Buttons**: Provides buttons to calculate and assign the quantity in kits, streamlining stock management.

Usage
=====

1. **Install the Module**:

   - Install the module through the Odoo apps interface or place it in your Odoo addons directory.

2. **Viewing Quantity in Kits**:

   - Navigate to the **Stock Replenishment Orderpoints**.
   - You will see a new field called **Quantity in Kits** displaying the relevant data.

3. **Calculating Quantity**:

   - Use the **Calculate Qty in Kits** button to compute the quantity of products in kits.
   - The **Assign Qty in Kits** button can be used to set the order quantity based on the kits.

Configuration
=============

- **No additional configuration is required** for this module. It automatically calculates and displays the kit quantities.

Testing
=======

Test the following scenarios:

- **Check Quantity in Kits**:

  - Go to the stock replenishment orderpoints and verify that the **Quantity in Kits** field displays the correct quantity.

- **Button Functionality**:

  - Click on the **Calculate Qty in Kits** button and verify that the quantity updates correctly.
  - Click on the **Assign Qty in Kits** button and ensure the order quantity is set as expected.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

For module-specific questions, please contact the contributors directly. Support requests should be made through the official channels.

License
=======

This project is licensed under the LGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
