# -*- coding: utf-8 -*-
# (c) 2017 Daniel Campos - AvanzOSC
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Supplierinfo Import",
    "version": "8.0.1.0.0",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Daniel Campos <danielcampos@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "purchase",
    "depends": ['purchase'],
    "data": ['wizard/import_price_file_view.xml',
             'views/product_pricelist_load_line_view.xml',
             'views/product_pricelist_load_view.xml',
             'security/ir.model.access.csv'
             ],
    "installable": True
}
