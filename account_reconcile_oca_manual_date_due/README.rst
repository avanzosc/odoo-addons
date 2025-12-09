.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================
Account Reconcile Oca Manual Data Due
=====================================

This module extends the **Bank Statement Line manual reconciliation** process to allow setting and propagating a custom *Expiration Date* (``manual_date_due``).

Key Features
============
- Adds a new field **Expiration Date (Manual)** in the reconciliation form of bank statement lines.
- Automatically retrieves the due date from the related move line (``date_maturity``).
- Propagates the selected due date into the reconciliation values.
- Ensures the due date is correctly transmitted during the manual reconciliation workflow.

Configuration
=============
1. Install the module.
2. Go to **Invoicing → Bank → Bank Statements**.
3. Open a statement line and use the **Manual Operation** tab.
4. Set the **Expiration Date (Manual)** if needed.
5. Validate reconciliation and check that the due date is applied.

Bug Tracker
===========
Bugs are tracked on `GitHub Issues <https://github.com/your-repo/account_bank_statement_manual_date_due/issues>`_.

Credits
=======
Contributors
------------

* Ane Gurruchaga <aneavanzosc@gmail.com>
* Ana Juaristi <anajuaristi@avanzosc.es>

Do not contact contributors directly for support or technical help.
