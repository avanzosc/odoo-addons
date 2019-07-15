# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Purchase With Invoice Last Price",
    "version": "8.0.1.0.0",
    'license': "AGPL-3",
    'author': "AvanzOSC",
    'website': "http://www.avanzosc.es",
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    "category": "Accounting & Finance",
    "depends": [
        "purchase",
        "account"
    ],
    "data": [
        "views/product_view.xml",
        "data/purchase_with_invoice_last_price_data.xml",
    ],
    "installable": True,
}
