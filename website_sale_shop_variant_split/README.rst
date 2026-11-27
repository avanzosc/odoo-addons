.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===============================
Website Sale Shop Variant Split
===============================

This module adds the "Split variants in shop" check to products (eCommerce
Shop section of the Sales tab) and to product attributes. When it is set on
a product, the online shop shows one product card per value of its split
attributes instead of a single card for the whole product.

The split attributes are the attributes with "Split variants in shop" set.
It is unset by default and can be set on any attribute that creates
variants. When a product
has several split attributes, there is one card per combination of their
values.

For each card, the module uses the first variant with those values:

* The image and the price of the card are the ones of that variant.
* The card links to the product page with that variant already selected.
* "Add to cart" from the card adds that variant, or opens the product
  configurator with that variant selected.
* "Add to wishlist" from the card adds that variant.

The extra cards count for the number of products and the pagination of the
shop. When the shop is filtered by values of a split attribute, only the
cards of those values are shown.

Products without split attributes are shown as usual, even when the check is
set.

Usage
=====

#. In Website > Configuration > Attributes, set "Split variants in shop" on
   the attributes to split by (e.g. Color).
#. Open a product with variants of those attributes.
#. In the Sales tab, eCommerce Shop section, set "Split variants in shop".
#. The online shop shows a card for each value of the split attributes.

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

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
