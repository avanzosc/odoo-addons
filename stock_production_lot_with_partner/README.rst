.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Stock production lot with partner
=================================

* In serial/lot numbers 3 new fields: Customer, supplier, and observations.
* When creating a lot/serial number, if it comes from "in" picking, assign the
  partner of the picking in the lot/serial number.
* When validating a "out" picking, if it includes products with serial numbers,
  for each one shipped, assign the customer of the picking to the lot/serial
  number.

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
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
