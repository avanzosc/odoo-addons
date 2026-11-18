# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Variant Export XLSX",
    "summary": "",
    "version": "18.0.1.0.0",
    "category": "Product",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product",
        "product_code_generator",
        "product_brand",
        "stock",
        "report_xlsx",
        "website_sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/product_product_xlsx_report.xml",
        "wizards/product_product_export_xlsx_report_views.xml",
    ],
    "external_dependencies": {
        "python": [],
    },
    "installable": True,
}
