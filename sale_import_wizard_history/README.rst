.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==========================
Sale Import Wizard History
==========================

This module extends ``sale_import_wizard`` to support historical sale order
imports and unified sales history analytics.

Main features
=============

* Adds a ``historical`` boolean flag on sale import headers.
* Splits import usability by menu:

  * Standard import action only shows records with ``historical = False``.
  * New historical import menu only shows records with ``historical = True``.
* Propagates ``historical`` to import lines (related field).
* Filters the "Imported Lines" shortcut by the current import mode
  (historical or non-historical).
* Hides ``Process`` action on historical imports.
* Extends sale import lines with additional business fields from XLS files
  (sales metadata, quantities, pricing, payment terms, etc.).
* Adds a new SQL report model (list + pivot) that unions:

  * real sale order lines (``sale.order.line``)
  * historical imported lines (``sale.order.import.line`` with ``historical=True``)
* Adds a smart button on partner form to open the unified history report
  filtered by the partner commercial entity.

Usage
=====

1. Go to the sale import wizard and create/import a file:
   * for normal flow, use "Import Sale Orders"
   * for historical data, use "Import Historical Sale Orders"
2. Validate imported lines.
3. Process is available only for non-historical imports.
4. Analyze mixed real + historical lines from:
   * Sales menu: ``Sales History Lines`` (list/pivot)
   * Partner smart button: ``Sales History``

Notes
=====

* Product and customer matching uses the base/import logic with module
  extensions.
* The unified report keeps the same select column order on both SQL branches
  to ensure pivot compatibility.
* Ordering is configured to show dated lines first (most recent first) and
  undated lines at the end.

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
* Eñaut Alberdi <enautavanzosc@gmail.com>
