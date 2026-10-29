.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================
Account Move Usability
======================

The **Account Move Usability** module improves the usability of accounting entries and invoices by enhancing payment order button visibility and ensuring consistent product selection across different navigation paths.

Features
========

- Automatically hides the **Add to Payment Order** button when the invoice payment status is **Blocked**.

- Displays the button again when the invoice is unblocked, provided that the standard visibility conditions are met.

- Preserves the existing button visibility conditions defined by the **Account Payment Order** module.

- Ensures that invoice lines use the actual invoice type (`move_type`) when determining the available products, regardless of how the invoice is accessed.

- Preserves the standard `default_move_type` fallback when the invoice type is not yet available.

- Fixes incorrect product filtering when accessing customer invoices through **Invoice Analysis** or **Journal Entries**, ensuring that sales products are displayed instead of purchase products.

Usage
=====

**Payment Order Button Visibility**

1. Navigate to **Accounting > Vendors > Bills**.

2. Open a posted vendor bill and select **Action > Block Payment**.

3. The **Add to Payment Order** button will automatically be hidden.

4. To unblock the invoice, select **Action > Unblock Payment**. The button will become visible again if the invoice meets the standard conditions.

**Invoice Product Selection**

1. Navigate to **Accounting > Reporting > Invoice Analysis** or **Accounting > Accounting > Journal Entries**.

2. Open an existing customer invoice and reset it to draft if necessary.

3. Add a new invoice line and select a product.

4. The product selection will correctly display products available for sale, regardless of the navigation path used to open the invoice.

5. Vendor bills will continue to display products available for purchase, preserving the standard behavior.

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

* Ana Juaristi <anajuaristi@avanzosc.es>
* Berezi Amubieta Eceiza <bereziamubieta@avanzosc.es>
