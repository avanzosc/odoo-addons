.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=======================
Account Audit Templates
=======================

This module provides technical UI visibility for accounting chart template
models in Odoo 14. It is intended for audit, review, and maintenance of PGCE/
chart template data that is usually hidden from standard functional menus.

Overview
========

The module adds a dedicated root menu named **Audit Templates** and exposes
list/form views for the following technical models:

* Configuration of Plans: ``account.chart.template``
* Account Templates: ``account.account.template``
* Group Hierarchy: ``account.group.template``
* Tax Templates: ``account.tax.template``
* VAT Repartition Lines: ``account.tax.repartition.line.template``
* Tax Groups: ``account.tax.group``
* Fiscal Positions: ``account.fiscal.position.template``
* Fiscal Position Tax Mapping: ``account.fiscal.position.tax.template``
* Fiscal Position Account Mapping: ``account.fiscal.position.account.template``

Key Features
============

* Centralized technical navigation under one accounting menu entry.
* Dedicated tree and form views for all relevant chart template models.
* Focused list columns for audit needs (for example: name, chart template,
  code/amount).
* Access restricted to ERP managers through model access rules.

Security
========

The module grants read/write/create/delete access on included models to:

* ``base.group_erp_manager``

Dependencies
============

* ``account``

Usage
=====

1. Install the module.
2. Go to Accounting and open **Audit Templates**.
3. Review or maintain template records from the corresponding submenu.

Translations
============

By design, source terms in the module are defined in English.
Localized UI labels should be provided through files in ``i18n/``.

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
* Aner Arregi <aneravanzosc@gmail.es>

License
=======

This project is licensed under AGPL-3.
