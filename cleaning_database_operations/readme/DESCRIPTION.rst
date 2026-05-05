This module provides a powerful tool for mass database cleanup in Odoo, designed
to remove historical records from multiple tables in a safe and controlled manner.

It deletes records from the following areas, filtered by company and creation
date:

- **Stock**: Stock Move Lines, Stock Moves, Stock Pickings, Stock Inventories,
  Stock Inventory Lines, Stock Quants, Stock Production Lots, Stock Valuation
  Layers.
- **Accounting**: Account Move Lines, Account Moves, Account Partial Reconciles,
  Account Payment Orders, Account Payment Lines, Bank Statements, Bank Statement
  Lines, Account Assets, Account Asset Lines, Account Check Deposits, Account
  Analytic Lines.
- **Sales**: Sale Orders, Sale Order Lines.
- **Purchases**: Purchase Orders, Purchase Order Lines.
- **Manufacturing**: MRP Workorders, MRP Productions.
- **Point of Sale**: POS Orders, POS Order Lines, POS Payments, POS Quotations,
  POS Quotation Lines, POS Sessions.
- **Transport**: Transport Carrier Lines to Invoice.

Key features:

- Deletion is performed using direct SQL in configurable batches (using CTEs) to
  avoid long table locks, statement timeouts, and WAL bloat.
- Each batch is committed independently, and ``VACUUM ANALYZE`` is executed after
  each table is cleaned.
- Foreign key references are safely handled by setting FK columns to ``NULL``
  before deleting parent records (e.g., POS orders).
- Optional compatibility with ``openupgradelib`` for logged queries.
- A cron job is provided to automatically execute scheduled cleanings every 30
  minutes.
- The module also supports resetting all sequences (``ir.sequence``) to 1.
