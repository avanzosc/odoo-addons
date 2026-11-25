.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==================================
Account Move Payment Days Analysis
==================================

## Features

- **Calculate Average Using** (`payment_days_basis`) selection on OCA payment modes: **Payment Date** or **Due Date**.
- Calculates payment days for posted vendor bills using the formula `max(0, selected_date - accounting_date)`.
- Uses the existing `full_reconcile_payment_date` field provided by the OCA `partner_time_to_pay` module.
- Stored computed field `days_until_payment` with the `avg` aggregation.
- Integrates **Days Until Payment** as an additional measure in the standard Odoo **Invoice Analysis** pivot view.
- No additional reports, actions, or menus are created.
- Due Date remains visible in the invoice form and list view, including paid invoices.
- Includes `days_until_payment_available` to identify invoices with valid dates for the calculation.

## Dependencies

- `account_payment_partner` from OCA/bank-payment, providing payment mode integration on invoices.
- `account_invoice_date_due` from OCA/account-invoicing, supporting invoice due date management.
- `partner_time_to_pay` from OCA/account-invoice-reporting, providing the computed `full_reconcile_payment_date` field.

Use the Odoo `18.0` branch of these modules.

The `partner_time_to_pay` dependency is responsible for determining the payment date based on accounting reconciliations. This addon reuses that field instead of implementing a separate payment date calculation.

## Payment Days Calculation

The calculation depends on the **Calculate Average Using** option configured on the invoice's payment mode.

### Payment Date

When set to **Payment Date**, the calculation uses `full_reconcile_payment_date`, provided by `partner_time_to_pay`.

```python
days_until_payment = max(
    0,
    (full_reconcile_payment_date - date).days,
)
```

The payment date is determined by the underlying module based on the invoice's accounting reconciliation information.

### Due Date

When set to **Due Date**, the calculation uses the invoice's `invoice_date_due`.

```python
days_until_payment = max(
    0,
    (invoice_date_due - date).days,
)
```

### General Rules

- Only posted vendor bills (`move_type == 'in_invoice'`) are considered.
- The accounting date (`date`) is used as the starting date.
- Negative results are converted to zero.
- The default calculation basis is **Due Date**.
- If the required date or payment mode is missing, `days_until_payment_available` is set to `False`.
- Invoices without valid calculation dates are excluded from the average.
- Changes to the payment mode configuration trigger recalculation of the stored payment days.

## Invoice Analysis Pivot

The module extends the standard Odoo 18 **Invoice Analysis** pivot view (`account.invoice.report`).

A new measure, **Days Until Payment**, is available in the existing pivot.

The measure uses the `avg` aggregation instead of `sum`.

No separate pivot report, window action, or menu is created.

### Average Calculation

The standard `account.invoice.report` model is based on invoice lines.

To prevent invoices with multiple lines from having a greater weight in the average, the module assigns the payment days value to only one invoice line.

Remaining lines contain `NULL` for this measure and are ignored by the SQL `AVG()` aggregation.

Invoices without valid payment days are also excluded from the average.

This provides an **unweighted average per invoice** for invoice-level groupings, such as vendor or accounting period.

### Pivot Limitations

Because the value is assigned to a single invoice line, the average may not accurately represent all invoices when grouping by invoice-line dimensions, such as product or product category.

The measure is intended primarily for invoice-level analysis.

## Installation

1. Install the required OCA dependencies from their `18.0` branches.
2. Copy `account_supplier_payment_days` into your Odoo `addons_path`.
3. Update the Apps list and install **Account Move Payment Days Analysis**.
4. Configure the **Calculate Average Using** option on each payment mode. The default is **Due Date**.
5. Open **Accounting > Reporting > Invoice Analysis**.
6. Select **Days Until Payment** from the available pivot measures.

## Limitations / Points to Validate

- Accounting reconciliations do not always represent actual bank payments. They may include offsets, discounts, or exchange differences. If the bank value date is required, a different date-selection policy must be defined.
- The payment date is determined by the `partner_time_to_pay` module. Partial payments and complete reconciliation follow the behavior implemented by that dependency.
- Only posted vendor bills are included in the payment days calculation.
- Bills without a payment mode or the required calculation date are marked as unavailable.
- The average is **unweighted per invoice**, not weighted by invoice amount.
- The average is designed for invoice-level groupings. Product-level or other invoice-line-based groupings may produce incomplete or misleading results.
- The confirming submission date and a custom XLSX audit export are **not** implemented.
- This addon has not been tested against a running Odoo 18 database. Installation testing and functional QA are required before production use.

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
