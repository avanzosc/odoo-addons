.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===================================
Account Penalty Active Subscription
===================================

This module extends **agreement** model to automatically compute and apply penalties when the number of active subscriptions linked to an agreement falls below the required minimum.

Features
--------

- Calculates penalties based on:
  - Required number of active subscriptions
  - Actual active subscriptions in progress
  - Penalty percentage and product price defined in the penalty type
- Generates `account.penalty` records when penalties apply.
- Integrates with agreement penalty lines to determine:
  - Penalty quantity (missing subscriptions)
  - Penalty amount (percentage × product price × missing units)
- Uses the appropriate sales journal based on the agreement’s sale type.

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



