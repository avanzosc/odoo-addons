.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Product Pricelist History
=========================

The **Product Pricelist History** module records changes made to price list rules in the chatter of the corresponding price list.

Whenever a price list item is created, modified, or deleted, the module generates an internal note containing the affected product and pricing information. Each message also records the user and the date and time of the operation through the standard Odoo chatter.

Features
========

- Records the creation of new price list rules.

- Records modifications made to existing price list rules.

- Records the deletion of price list rules.

- Displays the affected product, product template, product category, or global product scope.

- Shows the previous and new price when a pricing rule is modified.

- Supports fixed prices, percentage discounts, and formula-based pricing rules.

- Records changes to minimum quantities and validity dates.

- Uses the standard Odoo chatter to identify the user and the date and time of every operation.

- Formats monetary values using the currency configured on the price list.

Usage
=====

1. **Install the Module**:

   - Install the **Product Pricelist History** module from the Apps menu.

2. **Create a Price List Rule**:

   - Open a price list and add a new pricing rule.

   - When the rule is saved, an internal note is automatically added to the price list chatter.
   
   - The note displays the affected product and the configured price.

3. **Modify a Price List Rule**:
   
   - Change the price or any other tracked condition of an existing pricing rule.
   
   - The module automatically adds a message showing the previous value and the new value.
   
   - Example:
      Product: [PRODUCT01] Example Product
      Price condition: Fixed Price: €25.77 → Fixed Price: €26.77

4. **Delete a Price List Rule**:

   - When a pricing rule is deleted, the module records the affected product and its last configured price in the chatter.

5. **Audit Information**:
   
   - Every history message is linked to the corresponding price list.
   
   - Odoo automatically records the user and the date and time when the operation was performed.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Berezi Amubieta <bereziamubieta@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
