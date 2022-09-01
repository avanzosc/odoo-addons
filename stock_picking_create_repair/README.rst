.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===========================
Stock picking create repair
===========================

* In "Sale order type", "Product template", and "Picking", new field
"Is repair".
* When a "Service" type product is entered in a sales line, and this is a
"repair", the entry of the product to be repaired will be requested.
* When validating the sales order, if it is a repair type, an "Picking in" will
be created with the products to be repaired.
* When confirming an "Picking in", if it is a repair type, a repair order will
be created.
* At the end of the repair, a "Picking out" will be created.

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
