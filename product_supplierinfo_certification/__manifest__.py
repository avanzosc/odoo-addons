# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Supplierinfo Certification",
    "summary": "Customization Module",
    "version": "16.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": ["product", "purchase", "stock", "purchase_stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_supplierinfo_certification_views.xml",
        "views/res_partner_views.xml",
        "views/product_supplierinfo_views.xml",
        "views/stock_warehouse_orderpoint_views.xml",
    ],
    "installable": True,
}
