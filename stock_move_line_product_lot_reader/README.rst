.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==================================
Stock move line product lot reader
==================================

* In detailed operations of pickings new field "Reader", to read with a reader
  the "product", or "product lot", separated by a space.
* The product will be searched for by the "Internal Reference" field. If the
  product is not found, and it is an incoming delivery note, it will be
  searched in supplierinfo by the Vendor Product Code field.

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

* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
