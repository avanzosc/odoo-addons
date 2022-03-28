# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Thermoformed Cost Calculation",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Sales/CRM",
    "depends": [
        "mrp",
        "product",
        "sale_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/thermoformed_cost_calculation_sequence.xml",
        "data/thermoformed_cost_calculation_decimal.xml",
        "views/thermoformed_cost_views.xml",
        "views/res_company_views.xml",
        "views/frame_views.xml",
        "views/mrp_workcenter_views.xml",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "report/thermoformed_report_template.xml",
        "report/thermoformed_report.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
