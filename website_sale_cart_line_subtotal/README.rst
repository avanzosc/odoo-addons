.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Website Sale Cart Line Subtotal
===============================

Overview
--------

Adds Price Subtotal field to cart lines in website sale.

Features
--------

- Adds a "Price Subtotal" field to the cart lines in the website sale module.
- Calculates the subtotal by multiplying the product quantity by the list price.

Usage
-----

Once installed, the `website_sale_cart_line_subtotal` module will enhance the cart view in the website sale module by displaying the subtotal of each line item based on the product quantity and list price.

Technical Details
-----------------

- The module extends the `website_sale.cart_lines` view to include a new "Price Subtotal" column.
- It calculates the subtotal dynamically using Odoo's templating language (QWeb).

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
