.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===================================
Sale Order Commitment Date One Week
===================================

Overview
--------

The `sale_order_commitment_date_one_week` module is designed to automatically set the commitment date of a sale order to one week (7 days) after the order date. This functionality is useful for businesses that want to streamline their order processing by ensuring that a commitment date is always set, helping to manage customer expectations and improve order tracking.

Features
--------

- Automatically sets the commitment date to one week after the order date for each sale order.
- Provides a server action that can be executed to update the commitment date of existing sale orders.

Installation
------------

1. Place the module folder `sale_order_commitment_date_one_week` in your Odoo addons directory.
2. Update the Odoo module list by going to Apps -> Update Apps List.
3. Find the module `Sale Order Commitment Date One Week` and click on `Install`.

Usage
-----

1. Once the module is installed, it will automatically set the commitment date to one week after the order date for all new sale orders.
2. To update the commitment date of existing sale orders, you can use the provided server action:
    - Go to Sales -> Orders -> Quotations or Sales Orders.
    - Select the orders you want to update.
    - Click on `Action` and then `Set Commitment Date + 1 Week`.

Technical Details
-----------------

- The module extends the `sale.order` model by adding a method `set_commitment_date_one_week` which calculates and sets the commitment date.
- A server action is included to allow batch processing of sale orders to set their commitment dates.

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

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
