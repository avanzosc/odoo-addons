This module allows users to import supplier pricelists from CSV files directly
into Odoo.

It provides a wizard that reads a CSV file with supplier pricelist data,
validates the records (checking suppliers, products, and currencies), and
automatically creates `product.supplierinfo` records.

Key features include:

- CSV file upload with automatic parsing and field mapping.
- Validation of suppliers (by name), products (by barcode, internal reference,
  or name), and currencies (by ISO code).
- Batch creation of `product.supplierinfo` records with support for prices,
  discounts, minimum quantities, validity dates, and delivery lead times.
- Editable tree view to manually correct records before processing.
- Multi-company support via company scoping rules.
