.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================================
General Ledger Extended Account Filter
======================================


The **General Ledger Extended Account Filter** module extends the General Ledger report wizard by adding a new filter for customer advance accounts.

The module adds a new **Only Advance Accounts** checkbox in the account filters section. When selected, the accounts belonging to the Spanish accounting group **438 - Customer Advances** are automatically added to the account selection field.

The filter can be combined with the existing **Only Receivable Accounts** and **Only Payable Accounts** filters.

# Features

* Adds a new **Only Advance Accounts** checkbox to the General Ledger report wizard.

* Automatically selects accounts belonging to the accounting group **438 - Customer Advances**.

* Uses the standard account group created by the Spanish localization module **l10n_es**.

* Automatically removes the advance accounts from the account selection when the checkbox is disabled.

* Can be combined with the existing **Only Receivable Accounts** and **Only Payable Accounts** filters.

* Supports multi-company environments by using the corresponding accounting group of the selected company.

# Usage

1. **Install the Module**:

   * Install the **General Ledger Advance Account Filter** module from the Apps menu.

2. **Open the General Ledger Report**:

   * Go to **Accounting > Reporting > General Ledger**.

3. **Filter Advance Accounts**:

   * Open the **Account Filters** section.

   * Enable the **Only Advance Accounts** checkbox.

   * The accounts belonging to the accounting group **438 - Customer Advances** are automatically added to the account selection field.

4. **Combine Account Filters**:

   * The **Only Advance Accounts** filter can be used together with **Only Receivable Accounts** and **Only Payable Accounts**.

   * When several filters are enabled, the corresponding accounts are combined in the account selection field.

5. **Disable the Filter**:

   * Disable the **Only Advance Accounts** checkbox to remove the customer advance accounts from the account selection.


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
