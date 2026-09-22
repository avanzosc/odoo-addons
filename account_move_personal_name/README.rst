.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==========================
Account Move Personal Name
==========================

The **Account Move Personal Name** module adds a new field called **Personal Name** account moves.

The value is automatically generated when an invoice is posted and follows a company-specific sequential numbering format based on the invoice accounting date. The sequence is reset every year, producing identifiers such as **20260001**, **20260002**, etc.

Each company maintains its own independent sequence.

Features
========

- Adds a new **Personal Name** field to invoices.

- Automatically assigns the value when the invoice is posted.

- Generates a unique identifier using the accounting year and a sequential number.

- Maintains an independent sequence for each company.

- Automatically resets the sequence at the beginning of each year.

- Automatically creates the required sequence for existing and newly created companies.

Usage
=====

1. **Install the Module**:

   - Install the **Account Move Personal Name** module from the Apps menu.

2. **Invoice Posting**:

   - When an invoice is posted, the module automatically assigns a value to the **Personal Name** field.

3. **Sequence Format**:

   - The generated value consists of the accounting year followed by a four-digit sequential number.

   - Example:

     - 20260001
     - 20260002
     - 20260003

4. **Multi-company Support**:

   - Each company has its own independent sequence.

   - The sequence numbering restarts automatically for each new accounting year.

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
