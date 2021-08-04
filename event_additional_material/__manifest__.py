# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Additional Material",
    "version": "14.0.1.0.0",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "event_slides",
        "event_sale"
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/event_event_views.xml',
        'wizard/wiz_automatic_material_in_sale_order_views.xml',
    ],
    'installable': True,
}
