.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=========================================
Stock production lot warranty repair date
=========================================

* In products, new field "Repair warranty period (Months)".
* When validating an out picking that comes from a normal type order: update
  the guarantee date of all lots of the out picking, assigning the validation
  date + "Expiration time" of the product file.

* At the end of a repair, update the repair warranty date in the lot with date
  + "Repair warranty period (Months)" of the product file.

* If a repair is under warranty, mark it as non-billable.

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

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
