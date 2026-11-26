.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===============================
Stock Picking Package Usability
===============================

This module improves the usability of packages in stock pickings with the following
features:

- **Float dimensions**: overrides the OCA integer fields for length, width and height
  on both product packagings and quant packages, allowing decimal values.
- **Picking-to-package relationship**: adds a one-to-many link from a stock picking
  to its packages, with a smart button showing the package count and total weight.
- **Automatic package creation**: a *Number of Packages* field and a *Create Packs*
  button on the transfer form let users generate the required empty packages in one
  click. Packages are named automatically following the pattern ``{picking} - 001``.
- **Packaging synchronisation**: assigning a packaging to a move line propagates it
  to the destination package, and vice versa, keeping both in sync at all times.
- **Weight tracking**: each move line computes its own weight from product weight and
  quantity. The package aggregates all line weights plus the tare weight of its
  packaging, and exposes the total as shipping weight.
- **Volume summary**: total volume and weight of all packages are shown on the
  delivery carrier section of the transfer form.

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
* Lucía Echeverría <luciaecheverría@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
