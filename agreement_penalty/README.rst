.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=================
Agreement Penalty
=================

This module extends the **agreement** model to support per-agreement penalty configuration and provides the base infrastructure for creating ``account.penalty`` records from agreements.

**Features**

- New model ``agreement.penalty.type`` to link agreements with penalty types, storing per-line configuration:

  - Penalty type and its associated product (read-only, derived from the penalty type)
  - Penalty price (defaults to the product's sales price on selection)
  - Required active subscription count
  - Duration in months
  - Penalty percentage
  - Internal notes

- **Penalties** tab on the agreement form with an editable list of penalty lines
- Smart button on the agreement form showing the count of related penalties; opens the filtered penalty list
- ``apply_penalties()`` hook method on ``agreement``, designed as a stub to be overridden by specific penalty modules
- ``_check_existing_month_penalty(penalty_type_name)`` helper shared by all penalty modules: checks whether an ``account.penalty`` of the given type already exists for the current calendar month; returns ``True`` (skip) if it is already **invoiced**, deletes it and returns ``False`` if it is in **draft**, and returns ``False`` if none is found
- ``_get_penalty_journal()`` helper that resolves the appropriate sale journal from the agreement's sale type, falling back to the first available sale journal
- ``_create_account_penalty()`` helper that creates an ``account.penalty`` record linked to the agreement, used by all penalty modules that depend on this one
- Extends ``account.penalty`` with an ``agreement_id`` field and an ``affected_subscription`` count field
- Adds ``agreement_id`` and ``affected_subscription`` as optional columns to the penalty list view
- **Apply Penalties** server action available from the agreement form and list views
- Inactive monthly **cron job** (*Apply Penalties*) that calls ``apply_penalties()`` on all agreements; can be enabled to run the full penalty aggregation automatically — all penalty modules hooked into ``apply_penalties()`` are executed in a single run
- Adds an **Agreements** entry under the *Agreement Penalties > Operations* menu
- Security: ``agreement.penalty.type`` is readable by all internal users; full access (write, create, delete) restricted to system administrators

**Technical Details**

- **New model**: ``agreement.penalty.type``
- **Models extended**: ``agreement``, ``account.penalty``
- **Dependencies**: ``agreement``, ``account_penalty``

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
* Aner Arregi <aneravanzosc@gmail.com>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
