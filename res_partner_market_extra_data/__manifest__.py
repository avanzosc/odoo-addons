# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Res Partner Market Extra Data",
    "summary": "Technology For Customers",
    "version": "16.0.1.0.0",
    "category": "Sales/CRM",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "contacts",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_technology_views.xml",
        "views/res_partner_market_views.xml",
        "views/res_partner_state_views.xml",
        "views/res_partner_business_area_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_load_data",
}
