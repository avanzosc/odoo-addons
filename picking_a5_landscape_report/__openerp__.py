# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Picking A5 Landscape report",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Custom Module",
    "depends": [
        "stock_valued_picking_report",
        "sale_documents_comments",
    ],
    "data": [
        "data/report_paperformat.xml",
        "report/report_picking_a5_landscape.xml",
        "views/picking_a5_landscape_report.xml",
    ],
    "installable": True,
}
