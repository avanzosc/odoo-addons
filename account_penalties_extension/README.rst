.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===========================
Account Penalties Extension
===========================

This module extends the functionality of *Account Penalties* by adding automatic pricing logic and manual price overrides.

**Features**

- **Automatic Pricing**: Automatically fetches the sales price from the product associated with the selected Penalty Type.
- **Manual Price Override**: Allows users to manually modify the suggested penalty price for specific agreements.
- **Price Synchronization**: Automatically updates the final invoicing amount when the base price is modified.
- **Enhanced Views**: Displays the "Penalty Price" (base price) field in both form and tree views for better visibility.

**Main Functionality**

- **Smart Onchange**: When a Penalty Type is selected, the system looks up the related product's list price and populates the *Penalty Price* field.
- **Dynamic Amount Calculation**: The invoicing *Amount* is automatically synchronized with the *Penalty Price*.
- **Flexibility**: If a specific penalty requires a different amount than the standard product price, the user can edit the *Penalty Price*, and the system will update the final amount to be invoiced.

**Usage**

1. Create a new Penalty record.
2. Select a **Penalty Type** (e.g., "Early Termination").
3. The system automatically fills the **Penalty Price** and **Amount** based on the product's configuration.
4. If needed, manually edit the **Penalty Price**.
5. The **Amount** field updates automatically to match your manual entry.
6. Proceed to create the invoice as usual.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Authors
-------

* AvanzOSC

Contributors
------------

* Aner Arregi <aneravanzosc@gmail.com>
* Ana Juaristi <anajuaristi@avanzosc.es>

Maintainer
----------

This module is maintained by AvanzOSC.
