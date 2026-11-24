.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

========================
Account Delivery Amounts
========================

This module extends Odoo Invoicing (`account.move`) to automatically separate shipping-related amounts from product-related amounts within customer invoices.

It identifies shipping lines based on products configured in Delivery Carriers (`delivery.carrier`) and classifies invoice lines into shipping and non-shipping categories. This enables clear reporting and breakdown of logistics costs versus product sales.

Features
--------

- Automatically detects shipping products from Delivery Carrier configuration.
- Splits invoice lines into shipping and product categories.
- Computes separate totals for:
  - Shipping subtotal
  - Shipping taxes
  - Shipping total
  - Product subtotal
  - Product taxes
  - Product total
- Provides computed fields available directly on invoices (`account.move`).
- Enables use in reports, dashboards, and custom financial analysis.
- No impact on standard Odoo invoicing workflow.

Data Model
----------

**account.move**

- Shipping Subtotal (standard_shipping):
  - Sum of subtotal amounts for invoice lines related to shipping products.

- Shipping Taxes (tax_shipping):
  - Difference between shipping total and shipping subtotal.

- Shipping Total (total_shipping):
  - Sum of unit prices for shipping-related invoice lines.

- Product Subtotal (product):
  - Sum of subtotal amounts for non-shipping invoice lines.

- Product Taxes (product_tax):
  - Difference between product total and product subtotal.

- Product Total (product_total):
  - Sum of unit prices for non-shipping invoice lines.

Logic Overview
--------------

- Shipping products are retrieved from:
  `delivery.carrier.product_id`

- Invoice lines are evaluated:
  - If `line.product_id` is in shipping products → classified as shipping
  - Otherwise → classified as product

- Aggregation is performed per invoice (`account.move`), ensuring independent totals for each document.

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

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
