.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===========================
Stock Lot Move Line Company
===========================

* Lots/serial numbers created from a move line (for instance, when validating a
  receipt with "Create New Lots/Serial Numbers") take the company of the move
  line.
* By default, Odoo only sets a company on the new lot when the product belongs
  to a company. Lots of products shared between companies are created without
  company, and they cannot have the same name as a lot of that product in any
  company. This makes it impossible to receive, for instance, a unit for repair
  in one company when its serial number already exists in another company.
* Products that belong to a company keep the standard behaviour.

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

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
