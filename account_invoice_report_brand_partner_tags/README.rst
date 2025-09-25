.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================================
Acount Invoice Report Brand Partner Tags
========================================

Add **Product Brand** as a groupable dimension in the *Invoices Analysis* pivot
and provide custom filters for **Product Brand** and **Contact Labels**
(res.partner.category).

Key Features
============
- **Product Brand in Pivot**: adds a real ``brand_id`` column to
  ``account.invoice.report`` so you can *Group By → Product Brand*.
- **Brand filter**: filter invoices by product brand from the search bar.
- **Contact Labels filter**: filter by customer/vendor categories
  (contact tags) from the search bar.


Configuration
=============
1. Make sure the brand field exists on products:
   install the "module atharva_theme_general".
2. Install this module.
3. Go to **Accounting → Reporting → Invoices Analysis**.
4. Use the search bar:
   - **Product Brand** to filter by brand.
   - **Contact Labels** to filter by partner tags.
5. Use **Group By → Product Brand** in the pivot to analyze results by brand.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/avanzosc/odoo-addons/issues/new?body=module:%20account_banking_mandate_usability%0Aversion:%2014.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* AvanzOSC

Contributors
~~~~~~~~~~~~

* Ana Juaristi <anajuaristi@avanzosc.es>
* Ane Gurruchaga <aneavanzosc@gmail.com>

