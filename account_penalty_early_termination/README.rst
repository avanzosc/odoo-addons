.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=================================
Account Penalty Early Termination
=================================

This module extends the **sale.subscription** and **agreement** models to automatically apply **Early Termination** penalties when a subscription is closed before completing its required permanence period.

**Features**

- Hooks into ``set_close()`` on ``sale.subscription`` to detect early closures; only triggers for monthly subscriptions linked to an agreement
- Looks for an agreement penalty line whose penalty type is named **Early Termination**; if none is found, no penalty is created
- Calculates remaining months as: ``permanence_months − active_months``; skips the subscription if the permanence period was already met
- Calculates the penalty amount per subscription as: ``penalty_percentage × remaining_months × monthly_price`` (monthly price taken from the first recurring invoice line)
- Creates a ``subscription.penalty`` record per closed subscription storing the penalty amount, penalty months, and monthly price
- Hooks into ``apply_penalties()`` on the agreement to aggregate all early termination ``subscription.penalty`` records for the previous calendar month into a single ``account.penalty`` record
- Requires the agreement to have an **Early Termination** penalty line; skips the agreement otherwise
- Delegates duplicate-penalty detection to ``_check_existing_month_penalty()`` (provided by ``agreement_penalty``): if an early termination ``account.penalty`` already exists for the current month and is **invoiced**, the agreement is skipped; if it is in **draft**, it is deleted and recreated with current data
- Adds a **View Subscription Penalties** button on ``account.penalty`` records of type Early Termination to navigate to the underlying subscription penalties
- Adds penalty months, monthly price, and penalty amount columns to subscription penalty views
- The monthly cron job is provided by the ``agreement_penalty`` base module; enabling it there automatically triggers early termination penalty aggregation for all agreements

**Technical Details**

- **Models extended**: ``sale.subscription``, ``agreement``, ``account.penalty``, ``subscription.penalty``
- **Dependencies**: ``subscription_penalty``, ``agreement_penalty``, ``agreement_sale_creation``, ``agreement_livelink``

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
