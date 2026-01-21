.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=================
Account Penalties
=================

This module provides comprehensive penalty management and invoicing functionality within Odoo.

**Key Features**

- **Penalty Management**: Create and track penalty records with detailed information including quantity, amount, invoice date, partner, and journal
- **Penalty Types Management**: Configurable penalty types associated with service products
- **Predefined Penalty Types**: Two default penalty types: Early Termination and Device Not Returned
- **Invoice Generation**: Create invoices from penalties with one-click button for single or multiple selections
- **Smart Grouping**: Automatically groups penalties by partner and journal when creating invoices
- **Draft Invoice Reuse**: Automatically uses existing draft invoices for the same partner and journal
- **Status Tracking**: Visual status indicator (To Invoice / Invoiced) with automatic state updates

**Main Entities**

- **Penalty Records**: Complete penalty tracking including name, quantity, amount, invoice date, partner, journal, penalty type, and related product
- **Penalty Types**: Configurable types with name and associated product
- **Invoice Integration**: Direct link to generated invoices with automatic line creation

**Usage**

1. **Manage Penalty Types**: Go to Sales > Orders > Penalty Types to configure penalty categories
2. **Create Penalties**: Use the editable tree view to create penalty records quickly
3. **Set Details**: Specify partner, quantity, amount, invoice date, journal, and penalty type
4. **Generate Invoices**: 
   - Single: Click "Create Invoice" button on individual penalty
   - Multiple: Select multiple penalties and use "Create Invoice" from Actions menu
5. **Review**: System creates invoices grouped by partner and journal automatically

**Technical Details**

- **Models**: account.penalty, penalty.type
- **Views**: Editable tree views, form views with status bars, search views with filters
- **Dependencies**: account, sale, product, sales_team
- **Menu Locations**: 
  - Sales > Orders > Penalties
  - Sales > Orders > Penalty Types
- **Features**:
  - Multi-language support
  - Security rules for accounting and sales teams
  - Contextual actions for single and multiple records
  - Automatic currency handling from journal

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

Maintainer
----------

This module is maintained by AvanzOSC.
