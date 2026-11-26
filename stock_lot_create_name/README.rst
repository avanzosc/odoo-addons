.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
Stock lot create name
=====================

* In stock picking type, a new "Lot Code" field will be visible if the picking
  type, under "Lots/Serial Numbers", is marked as "Create New".
* When a picking is validated and it has a picking type with a defined
  "Lot Code", and the stock move line is to be created, and this has a product
  with lot tracking, the move line will be named "lot_name" with the code of
  the delivery note type + part of the delivery note name.

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
