.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================================
Account Bank Statement Partner Autofill
=======================================

This module extends the behavior of bank statement line creation and reconciliation in Odoo.

* When importing a bank statement, if a line has the same *payment reference* as a previous reconciled line,
  the system automatically assigns the same customer (``partner_id``) to the new line.
* When a statement line is reconciled and has a ``partner_id`` set,
  all other lines with the same *payment reference* and no ``partner_id`` are updated automatically.

This feature avoids the need to manually assign the same customer each time
for recurring bank movements that use consistent descriptions in the bank extract.

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
~~~~~~~~~~~~

* Ana Juaristi <anajuaristi@avanzosc.es>
* Ane Gurruchaga <aneavanzosc@gmail.com>
