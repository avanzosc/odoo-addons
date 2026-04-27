.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================
Sale Import Wizard DRC
======================

This module extends ``sale_import_wizard_history`` to support DRC-specific XLS
imports.

Main features
=============

* Adds explicit mapping for these Excel columns:

  * ``Origin``
  * ``Equipo de ventas (team_id)``
  * ``Currency Code``
  * ``Entity Discount Percent``
  * ``QuantityInvoiced``
  * ``QuantityPacked``
  * ``Usage unit (UOM)``
  * ``Warehouse Name``
  * ``Discount``
  * ``Sales Person``
  * ``Payment Terms``
  * ``Payment Terms Label``
* Extends the import ``Help`` tab to show those column names.

Usage
=====

1. Go to Sales import and create a new import batch.
2. Load an XLS file including the supported DRC columns above.
3. Import and validate lines.
4. Check the imported line values and continue with the normal process flow.

Notes
=====

* This module depends on ``sale_import_wizard_history``.
* Column names are matched exactly as written in the list above.

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
