.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=================================
Account Penalty Early Termination
=================================

This module extends **sale.subscription** and **agreement** models to automatically apply **Early Termination** penalties when a subscription is closed before meeting its required permanence period.

Features
--------

- Automatically detects subscription closures and creates a penalty record when applicable.
- Prevents duplicate penalties for the same subscription and date.
- Calculates penalty amounts based on:
  - Permanence months
  - Percentage defined in the penalty type
  - Monthly recurring price of the subscription
- Integrates with Agreements:
  - Aggregates penalties from all closed subscriptions linked to an agreement.
  - Creates `account.penalty` records with the computed totals.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/mrp-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.



