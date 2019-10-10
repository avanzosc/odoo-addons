# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Partner Locker Room",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "contacts",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Customer Relationship Management",
    "data": [
        "security/partner_locker_room.xml",
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/partner_locker_room_view.xml",
        "views/partner_locker_room_shelf_date_view.xml",
        "wizard/wiz_assign_shelf_view.xml",
        "wizard/wiz_desassign_shelf_view.xml",
    ],
    "installable": True,
}
