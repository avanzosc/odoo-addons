# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Thermoformed Cost Calculation",
    "version": "16.0.2.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales/CRM",
    "depends": [
        "mrp",
        "product",
        "sale_management",
        "sale_order_offer_version",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/thermoformed_cost_calculation_sequence.xml",
        "data/thermoformed_cost_calculation_decimal.xml",
        "views/thermoformed_cost_views.xml",
        "views/res_company_views.xml",
        "views/frame_views.xml",
        "views/mrp_workcenter_views.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "report/thermoformed_report_template.xml",
        "report/thermoformed_report.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
