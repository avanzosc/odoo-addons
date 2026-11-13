.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Contact Supplier Payment Term Access
====================================

This module extends Odoo Contacts (`res.partner`) to allow users without Accounting permissions to view supplier payment terms.

By default, the Supplier Payment Terms field (`property_supplier_payment_term_id`) is only visible to users belonging to specific Accounting security groups.

This module introduces an independent security group that grants access to this field without requiring users to have Accounting or Invoicing permissions.

## Features

- Adds a new security group: **View Supplier Payment Terms**.
- Allows users without Accounting permissions to view supplier payment terms on contact forms.
- Extends the standard Odoo Contacts form view.
- Preserves existing visibility for users with Accounting permissions.
- Does not grant additional Accounting or Invoicing access rights.
- Does not modify the standard supplier payment terms functionality.
- Compatible with Odoo 18.

## Security Groups

**View Supplier Payment Terms**

- Technical ID: `res_partner_supplier_payment_term_access.group_view_supplier_payment_term`
- Grants visibility to the Supplier Payment Terms field on contact forms.
- Can be assigned independently of Accounting or Invoicing security groups.
- Does not inherit any Accounting permissions.

## Data Model

**res.partner**

- Supplier Payment Terms (`property_supplier_payment_term_id`):
  - Existing standard Odoo field.
  - Defines the payment terms applied to supplier transactions.
  - Becomes visible to users assigned to the new security group.
  - Retains its standard behavior and company-dependent configuration.

## Logic Overview

- The module inherits the standard Odoo view:
  - `account.view_partner_property_form`

- The visibility restriction of `property_supplier_payment_term_id` is extended to include:
  - `account.group_account_invoice`
  - `account.group_account_readonly`
  - `res_partner_supplier_payment_term_access.group_view_supplier_payment_term`

- Users belonging to any of these groups can access the field on the contact form.

- Users without these groups cannot see the field.

- No additional model access rights or Accounting permissions are introduced.

- The field remains editable according to the user's existing permissions on `res.partner`.

Bug Tracker
===========


Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Berezi Amubieta <bereziamubieta@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
