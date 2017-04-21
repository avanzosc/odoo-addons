# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Sale Service Recurrence Configurator',
    'version': '8.0.1.1.0',
    'category': 'Website',
    'license': "AGPL-3",
    'author': "AvanzOSC",
    'website': "http://www.avanzosc.es",
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    'depends': [
        'product',
        'website_quote',
    ],
    "data": [
        "views/sale_quote_view.xml",
        "views/sale_order_view.xml",
        "views/product_template_view.xml",
    ],
    "installable": True,
}
