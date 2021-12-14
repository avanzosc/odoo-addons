# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "School Permissions Age",
    "version": "12.0.1.0.0",
    "category": "Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contacts_school_permission",
        "partner_contact_birthdate",
    ],
    "data": [
        "views/res_partner_permission_view.xml",
        "views/res_partner_permission_type_view.xml",
    ],
    "installable": True,
}
