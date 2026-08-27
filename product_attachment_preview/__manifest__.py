# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Attachment Preview",
    "version": "16.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/avanzosc/odoo-addons",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "security/product_attachment_preview.xml",
        "security/ir.model.access.csv",
        "views/product_product_views.xml",
    ],
    "installable": True,
}
