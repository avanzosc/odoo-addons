# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contact's birthdate reminder",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contacts",
        "partner_contact_birthdate",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/res_partner_birthdate_report_view.xml",
        "reports/res_partner_birthday_report_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
