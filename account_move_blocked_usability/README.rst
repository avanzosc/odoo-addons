.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==============================
Account Move Blocked Usability
==============================

The **Account Move Blocked Usability** module improves the management of blocked invoices by automatically hiding the **Add to Payment Order** button when an invoice has its payment status set to **Blocked**.

This prevents users from manually adding blocked invoices to payment orders through the invoice form, while preserving the standard button visibility conditions.

Features
========

- Automatically hides the **Add to Payment Order** button when the invoice payment status is **Blocked**.

- Displays the button again when the invoice is unblocked, provided that the standard visibility conditions are met.

- Preserves the existing button visibility conditions defined by the **Account Payment Order** module.

Usage
=====

1. **Install the Module**:

   - Install the **Account Move Blocked Usability** module from the Apps menu.

2. **Block an Invoice**:

   - Navigate to **Accounting > Vendors > Bills**.

   - Open a posted vendor bill and select **Action > Block Payment**.

   - The **Add to Payment Order** button will automatically be hidden.

3. **Unblock an Invoice**:

   - Open a blocked vendor bill and select **Action > Unblock Payment**.

   - The **Add to Payment Order** button will become visible again if the invoice meets the standard conditions.

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
