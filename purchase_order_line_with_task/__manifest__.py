# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Purchase Order Line With Task",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Purchases",
    "depends": [
        "account_invoice_task",
        "purchase",
    ],
    "data": [
        "views/project_task_views.xml",
        "views/purchase_order_line_views.xml",
    ],
    "installable": True,
}
