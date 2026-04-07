.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===============================
Stock picking create repair woo
===============================

* In product new field "Generic Repair Product".
* When a sales order line is created, and the product is a repair service, a
  product with "Generic Repair Product" will be searched for, and the repair
  product will be placed in the sales order line.
* When confirming an incoming picking, belonging to a repair, it will be
  validated that in said picking there is no product with "Generic Repair
  Product".
* In an incoming picking, if in any movement a product with "Generic Repair
  Product" is modified by another product, and this move is associated with a
  sales line, the new product assigned to the move will be placed in the
  "product to be repaired" of the sales order line.

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

* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
