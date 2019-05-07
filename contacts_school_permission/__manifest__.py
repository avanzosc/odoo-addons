# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "School Permissions",
    "version": "12.0.1.0.0",
    "category": "Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contacts",
        "contacts_school",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/res_partner_permission_view.xml",
        "views/res_partner_permission_type_view.xml",
    ],
    "installable": True,
}
