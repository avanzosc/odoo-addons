# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Zone for partner",
    "version": "14.0.1.0.0",
    "category": "Generic Modules",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contacts",
        "sales_team"
    ],
    "data": [
        "views/partner_view.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
        "demo/zone_demo.xml"
    ],
    "installable": True,
}
