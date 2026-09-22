.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Account Move Shopify Payment Gateway
====================================

This module extends the Odoo Accounting model to improve traceability between invoices and Shopify payment gateways.

It introduces a computed relationship that links customer invoices (account.move) with the Shopify payment gateways used in the originating sales orders, ensuring financial documents retain full visibility of the payment method used in the eCommerce flow.

Features
--------

- Adds computed field on invoices to track related Shopify payment gateways.
- Automatically retrieves gateways from sales orders linked through invoice lines.
- Ensures deduplicated and clean gateway aggregation.
- Provides full traceability from invoice to Shopify payment processing.

Data Model
----------

**account.move**

- Shopify Payment Gateways (shopify_payment_gateway_ids)
  - Computed Many2many field that links invoices to Shopify payment gateways.

Purpose
-------

In standard Odoo Shopify integrations, invoice records do not always preserve explicit references to the payment gateway used at the time of order creation.

This module solves that limitation by:

preserving payment gateway traceability at invoice level
enabling reporting based on Shopify payment methods
improving reconciliation and financial analysis in multi-gateway setups

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* AvanzOSC

Contributors
~~~~~~~~~~~~

* `AvanzOsc <http://www.avanzosc.es>`_:

  * Berezi Amubieta <bereziamubieta@avanzosc.es>
  * Ana Juaristi <anajuaristi@avanzosc.es>
