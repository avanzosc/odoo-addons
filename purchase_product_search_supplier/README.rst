.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

================================
Purchase Product Search Supplier
================================

Changes the product search order in purchase order lines,
prioritizing supplier pricelists (supplierinfo) over internal references.

Search order:
1. Supplier code/name in supplierinfo
2. Exact internal reference (`default_code`)
3. Exact barcode
4. Partial internal reference + partial product name
5. Code in brackets `[REF]`

The new search order is only activated in the purchase order context (`from_purchase: True`).
Any other model (sales, inventory, invoices, etc.) keeps the standard Odoo behavior unchanged.

The supplier filter is strict: only supplierinfo records matching the vendor
selected in the purchase order are considered in step 1.
If no vendor is selected, step 1 is skipped entirely.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.



