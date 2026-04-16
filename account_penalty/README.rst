.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=================
Account Penalties
=================

This module provides penalty management and invoicing functionality within Odoo.

**Key Features**

- **Penalty Management**: Create and track penalty records with detailed information including name, quantity, amount, invoice date, partner, journal, and penalty type
- **Penalty Types Management**: Configurable penalty types, each linked to a service product
- **Predefined Penalty Types**: Two default penalty types installed with demo data: Early Termination and Device Not Returned
- **Invoice Generation**: Create invoices from penalties with a one-click button on individual records or via the Actions menu for multiple selections
- **Smart Grouping**: Automatically groups selected penalties by partner and journal when creating invoices; the invoice date used is the latest date among the grouped penalties
- **Status Tracking**: Visual status indicator (To Invoice / Invoiced) that updates automatically when an invoice is linked

**Main Entities**

- **Penalty Records** (``account.penalty``): Tracks name, quantity, amount, invoice date, partner, journal, penalty type, related product (read-only, from the penalty type), and the generated invoice
- **Penalty Types** (``penalty.type``): Configurable types with a name and an associated product

**Usage**

1. **Manage Penalty Types**: Go to *Agreement Penalties > Settings > Penalty Types* (or *Sales > Configuration > Penalties > Penalty Types*) to configure penalty categories
2. **Create Penalties**: Go to *Agreement Penalties > Operations > Agreement Penalties* (or *Sales > Orders > Penalties*) and use the editable tree view to create records quickly
3. **Set Details**: Specify partner, quantity, amount, invoice date, journal (sale journals only), and penalty type
4. **Generate Invoices**:

   - **Single**: Click the *Create Invoice* button on an individual penalty record
   - **Multiple**: Select multiple penalties in the list and use *Create Invoice* from the Actions menu

5. **Review**: The system creates one invoice per partner/journal combination, using the latest invoice date in each group

**Technical Details**

- **Models**: ``account.penalty``, ``penalty.type``
- **Views**: Editable tree view, form view with status bar, search view with filters and group-by options
- **Dependencies**: ``account``, ``sale``, ``product``, ``sales_team``
- **Menu Locations**:

  - *Agreement Penalties > Operations > Agreement Penalties*
  - *Agreement Penalties > Settings > Penalty Types*
  - *Sales > Orders > Penalties*
  - *Sales > Configuration > Penalties > Penalty Types*

- **Security**: Full access (read, write, create, delete) granted to ``account.group_account_user`` and ``sales_team.group_sale_manager``

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Authors
-------

* AvanzOSC

Contributors
------------

* Aner Arregi <aneravanzosc@gmail.com>
* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Maintainer
----------

This module is maintained by AvanzOSC.
