.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

====================
SPF Pricelist Import
====================

This module imports Shopify market prices into Odoo sale pricelists. It allows
each pricelist to be linked to a Shopify market, such as Spain, UK, or ROW, so
the importer can map columns like ``Price / Spain`` and
``Compare At Price / Spain`` to Odoo pricelist rules.

The importer lets users select web catalogs. The selected catalogs are copied
to every generated import line and assigned to the created or updated pricelist
items.

Key features:

* Create and assign Shopify markets to pricelists.
* Assign one or more web catalogs to imported pricelist items.
* Add a **PVP** field on pricelist rules, used to migrate v12 HLC information.
* Add a **Distribution Price** field on pricelist rules.
* **Import** Shopify prices from an ``.xlsx`` file using market columns.
* Review imported lines before processing them, following the
  ``base_import_wizard`` flow.
* Update existing active pricelist rules when they already exist for the same
  pricelist, market, and product.
* Create a new pricelist rule when existing rules for that product are expired.

Usage / How to test
===================

Backend
-------

1. Go to **Sales → Products → Pricelist Markets**.
2. Create the Shopify markets used in the spreadsheet, for example ``Spain``,
   ``UK`` and ``ROW``.
3. Go to **Sales → Products → Pricelists** and open a pricelist.
4. Set the **Market** field.
5. Go to **Imports → Import Pricelist Items** and create a new import.
6. Upload the Shopify ``.xlsx`` file and optionally select **Catalogs**. Click
   **Import** to generate import lines with those catalogs.
7. Click **Validate** to check products and whether each line will
   create or update a pricelist rule.
8. Review possible errors in the import lines or error log.
9. Click **Process** to create/update the pricelist rules.
10. Check the pricelist rules. ``Compare At Price / Market`` is imported as the
   fixed price when it has a value, and ``Price / Market`` is imported as
   distribution price. If ``Compare At Price / Market`` is empty, both fields
   receive ``Price / Market``.

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

* Ane Gurruchaga <aneavanzosc@gmail.com>
* Ana Juaristi <anajuaristi@avanzosc.es>
