.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=============================
Sale Product Attribute Hidden
=============================

This module adds the "Hide in product configuration" check to product
attributes that never create variants. It is meant for attributes that are
only used to classify and filter products, not to be chosen when selling.

The values of a hidden attribute are kept on the products, but:

* The variant grid of sales and purchase orders does not use them as rows or
  columns. The grid only shows the attributes that make the variants.
* The product configurator and the combo configurator of sales orders do not
  ask for them, and their extra prices are not added.
* A product whose only attributes with several values are hidden is added to
  the order directly, without opening the grid or the configurator.
* The product page of the online shop does not show them.
* They are not added to the order lines nor to their description.

The products can still be filtered by the values of a hidden attribute in the
online shop.

Attributes that create variants cannot be hidden.

Usage
=====

#. Go to Sales > Configuration > Attributes and open an attribute whose
   variants creation mode is "Never".
#. Set "Hide in product configuration".

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
