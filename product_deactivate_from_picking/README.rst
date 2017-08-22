.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===============================
Product deactivate from picking
===============================

* Define in products whether it is unique or not.
* When transferring an output picking, the transferred product is unique, and
  has a stock to zero, the product will automatically be deactivated, and a
  message will be created in this product.
* When a return is sent from an output picking, and the product is unique, and
  is deactivated, the product is automatically activated, and a message is
  created in the product.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
