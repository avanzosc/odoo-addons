.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=========================================
Website Sale Partner Category Restriction
=========================================

This module restricts which payment providers and delivery methods each
customer can use, based on the customer tags (``res.partner.category``).

A "Customer Tags" field is added to:

* Payment providers (Configuration tab, Availability section).
* Delivery methods (Availability tab, Customers section).

When the field is empty, the provider or delivery method is available to
every customer, as in standard Odoo. When it has tags, it is only
available to customers that have at least one of them. The tags of the
customer itself and those of its company (commercial partner) are both
taken into account, so contacts inherit the tags of their company.

Scope:

* Payment providers are filtered wherever Odoo computes the compatible
  providers: eCommerce checkout, payment of quotations/orders and invoices
  from the customer portal, and payment links.
* Delivery methods are filtered only on the eCommerce checkout. Backend
  users can still choose any delivery method on sale orders.

The standard availability rules (company, countries, currencies, maximum
amount, weight, product tags...) still apply on top of this filter.

Usage
=====

#. Create a tag per payment provider / delivery method, e.g.
   ``Web / Payment SEPA`` or ``Web / Delivery GLS``.
#. Set those tags in the "Customer Tags" field of the payment provider or
   delivery method.
#. Add the tags to the customers (or to their company). Tags can be set in
   bulk from the customer list view.

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
