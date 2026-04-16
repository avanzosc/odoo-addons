.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===================================
Account Penalty Active Subscription
===================================

This module extends the **agreement** model to automatically compute and apply penalties when the number of active subscriptions linked to an agreement falls below the required minimum.

**Features**

- Hooks into the ``apply_penalties()`` method on agreements to trigger active-subscription penalty evaluation
- Counts inactive subscriptions for an agreement as those with stage ``Closed`` and ``Pending Activation``
- Looks for a penalty line on the agreement whose penalty type is named **Active Subscriptions**; if none is found, no penalty is created
- Calculates the number of missing subscriptions as: required count (from the penalty line) minus actual inactive count
- Calculates the penalty amount as: ``penalty_percentage × penalty_price × missing_subscriptions``
- Delegates duplicate-penalty detection to ``_check_existing_month_penalty()`` (provided by ``agreement_penalty``): if an active-subscription ``account.penalty`` already exists for the current month and is **invoiced**, the agreement is skipped; if it is in **draft**, it is deleted and recreated with current data
- Creates an ``account.penalty`` record storing the penalty amount and the number of affected subscriptions (missing count)
- Resolves the sales journal from the agreement's sale type; falls back to the first available sale journal
- The monthly cron job is provided by the ``agreement_penalty`` base module; enabling it there automatically triggers active-subscription penalty evaluation for all agreements

**Technical Details**

- **Model extended**: ``agreement``
- **Dependencies**: ``agreement_penalty``, ``agreement_sale_creation``, ``agreement_livelink``

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
