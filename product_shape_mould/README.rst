.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
Product Shape Mould
===================

This module adds master tables for product shapes, moulds, and templates.

The following information is stored for each shape:

* Brand information.
* Shape code.
* Mould.
* Length, width, nose, tail, and wheelbase in millimeters.
* Length, width, nose, tail, and wheelbase in inches.

The shape code must be unique. The mould is automatically calculated from the
first three characters of the shape code.

A shape always has a mould and can optionally be linked to a template.

Moulds and templates share the same table. Each record stores its type, code,
group, subgroup, and description. Separate menus display each type and provide
the corresponding default during standard Odoo imports.

The module adds the mould technical data to each lot or serial number whose
product is marked as a mould.


Usage
=====

1. Go to **Manufacturing → Configuration → Templates and Moulds → Shapes**.
2. Create or edit the product shapes and their measurements.


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
