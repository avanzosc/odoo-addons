This module is designed for companies that need to import large volumes of
vendor pricelists from external sources (e.g., spreadsheets or ERP exports)
into Odoo.

Typical use cases include:

- Onboarding new suppliers with hundreds of products and prices.
- Periodic price updates received as CSV files from vendors.
- Migrating supplier information from a legacy system to Odoo.

The module relies on the `base_import_wizard` framework from OCA, which
provides the underlying file upload, CSV parsing, and batch validation
infrastructure.
