.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=========================
Purchase order report fix
=========================

This module fixes purchase PDF addresses and replaces the address block
with an improved version:

* Left column: shipping address. It uses ``dest_address_id`` when defined,
  otherwise the warehouse partner from
  ``picking_type_id.warehouse_id.partner_id``.
* Right column: supplier address including VAT/Tax ID when available.

It also disables the standard ``purchase_stock`` report inheritance to avoid
duplicated shipping address blocks.

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
