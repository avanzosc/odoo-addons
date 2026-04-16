.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

====================
Subscription Penalty
====================

This module introduces a new model to register penalties applied to subscriptions, including the penalty type and the date it was applied.

**Features**

- New ``subscription.penalty`` model linked to ``sale.subscription``; records are deleted automatically when the subscription is deleted
- Fields: subscription, penalty type, and applied date
- Tree, form, and search views for ``subscription.penalty``, with group-by options by subscription, penalty type, and applied date
- **Penalties** tab inside the subscription form with an editable list of penalty records
- Menu entries:

  - *Subscriptions > Subscription Penalties*
  - *Agreement Penalties > Operations > Subscription Penalties*
  - *Agreement Penalties > Operations > Subscriptions*

- Security: full access (read, write, create, delete) granted to all internal users

**Technical Details**

- **New model**: ``subscription.penalty``
- **Model extended**: ``sale.subscription``
- **Dependencies**: ``sale_subscription``, ``account_penalty``

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
