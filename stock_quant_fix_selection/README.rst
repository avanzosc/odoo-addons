.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=========================
Stock quant fix selection
=========================

* When quants are selected to display quantities of the product. Take into
  account that the quant creation date must be >= the product creation date.
* If by context they pass us the value "to_date", take this date into account
  when selecting the quants.
* If by context they pass us the value "from_date", take this date into account
  when selecting the quants.

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
