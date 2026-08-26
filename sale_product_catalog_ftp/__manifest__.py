# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Catalog FTP Sync",
    "summary": "Daily xlsx stock export per customer, uploaded to their FTP server",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "sale_product_catalog",
        "stock_b2b_availability",
        "report_xlsx",
        "product_brand",
        "product_pricelist_import_spf",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_catalog_ftp_views.xml",
        "reports/report_actions.xml",
        "data/ir_cron.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "installable": True,
}
