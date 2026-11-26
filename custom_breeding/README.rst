.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===============
Custom Breeding
===============

This module extends the **res.partner** model to include additional fields for accounting management and external system integration.

Features
--------

- Adds new fields to partners:
  - Leaving Date
  - Eurowin Account
  - Purchase Journal (limited to purchase journals)

- Updates partner views:
  - Displays the new fields in the form view.
  - Adds Eurowin Account and Journal in the list view.
  - Enables filtering and grouping by Purchase Journal.
  - Shows partner reference in kanban view.

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
* Ana Juaristi <anajuaristi@avanzosc.es>
