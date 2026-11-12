.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===================================
Account Financial Report In Payment
===================================

The **Account Financial Report In Payment** module extends the Open Items report from the OCA **account_financial_report** module by including invoices that are currently in the **In Payment** state.

By default, the Open Items report excludes fully reconciled journal items, even when their associated invoices are still in the **In Payment** state.

This module extends the report to include these invoices when their due date is later than the current date, even if their journal items are fully reconciled.

The standard behavior of the Open Items report is preserved, and the additional invoices are displayed without modifying their original accounting residual amounts.

# Features

* Extends the **Open Items** report to include invoices in the **In Payment** state.

* Includes fully reconciled journal items associated with invoices whose due date is later than the current date.

* Supports both **Customer Invoices** and **Vendor Bills**.

* Preserves the standard Open Items report behavior for unreconciled journal items.

* Maintains the original accounting residual amounts without modifying the report totals.

* Identifies the additional invoices with an **[In payment]** label in the report reference.

* Respects the company and account filters selected in the report wizard.

* Applies the extended functionality automatically without requiring additional configuration.

# Usage

1. **Install the Module**:

   * Install the **Account Financial Report In Payment** module from the Apps menu.

2. **Open the Open Items Report**:

   * Go to **Accounting > Reporting > Open Items**.

3. **Generate the Report**:

   * Select the desired company, accounts, and report date.

   * Generate the report using the standard Open Items wizard.

4. **View In Payment Invoices**:

   * The report automatically includes invoices that meet the following conditions:

     * The invoice is posted.

     * The payment state is **In Payment**.

     * The associated journal item is fully reconciled.

     * The due date is later than the current date.

   * These invoices are displayed alongside the standard unreconciled journal items.

5. **Review the Report Results**:

   * Additional invoices are identified with an **[In payment]** label.

   * Their original accounting residual amounts are preserved.

   * The report totals remain unchanged, ensuring consistency with the accounting balances.

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
