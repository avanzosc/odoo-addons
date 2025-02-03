.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=====================================
Product pricelist last purchase price
=====================================

* In partner new fields: "Not Update Price From Order", and "Not Update Price
  From Invoice". These 2 fields are of type "related" in "Supplier Pricelist".
* When a purchase order is confirmed, the supplier/product exists in "Supplier
  Pricelist", and is not marked as "Not Update Price From Order", information
  will be updated in "Supplier Pricelist".
* When a supplier invoice is confirmed, and the supplier/product does not exist
  in "Supplier Pricelist", the information will be posted in "Supplier
  Pricelist".
* When a supplier invoice is confirmed, the supplier/product exists in "Supplier
  Pricelist", and is not marked as "Not Update Price From Invoice", information
  will be updated in "Supplier Pricelist".


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
