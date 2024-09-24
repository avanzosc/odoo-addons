# Copyright 2018 Maite Esnal - AvanzOSC
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Partner Characterization",
    "version": "16.0.1.0.0",
    "category": "Customers, Vendors, Partners,...",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "contacts",
        "base_characterization",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/partner_view.xml",
        "views/partner_characterization_view.xml",
        "views/res_partner_economic_data_view.xml",
    ],
    "installable": True,
}
