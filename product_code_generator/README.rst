.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

======================
Product Code Generator
======================

This module builds an automatic product reference (``default_code``) out
of four classification segments on the product template:

* Brand (``product.brand``, from the ``product_brand`` OCA module) - 2
  digit code.
* Family (``product.category``, root level) - 2 digit code.
* Subfamily (``product.category``, child level) - 2 digit code.
* Season (``seasonality``, from the ``product_simple_seasonality`` OCA
  module) - 3 digit code.

Each of those models gets a ``code`` field (auto zero-padded to its
fixed width; the category one also auto-fills from the category name
when left empty). Concatenating the four codes gives a 9-character
prefix. The first product coded with a given combination creates a
``product.code`` record for that prefix, together with a dedicated
``ir.sequence`` (3-digit padding, no gaps). Every following product
with the same brand/family/subfamily/season reuses that same sequence,
so ``default_code`` values for one combination are consecutive.

Use the "Generate Code" button on the product form (only shown while
``default_code`` is empty) to fill it in from the product's brand,
family, subfamily and season.

The "Product Codes" screen (Sales > Configuration > Products) lists the
generated prefixes and lets an admin adjust the next number of the
underlying sequence.

Barcodes
========

Every product variant gets an EAN13 barcode auto-generated on creation
(and via the "Generate Code" button, for existing variants without
one) when it isn't given explicitly:

* ``res.company.barcode_prefix`` (7 digits max, configurable on the
  company form) provides the first segment.
* A dedicated ``ir.sequence`` (``barcode.sequence``, company-aware,
  5-digit padding) provides the next 5 digits.
* The 13th digit is the standard EAN13 check digit.

A company without a barcode prefix set will get an error when a
product is created without an explicit barcode, instead of silently
skipping barcode generation.

Product import
===============

Adds a "Season Name" / "Season" pair of columns to the product variant
importer (``product_import_wizard``), following the same
name-then-resolve pattern already used there for the product category.

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

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
