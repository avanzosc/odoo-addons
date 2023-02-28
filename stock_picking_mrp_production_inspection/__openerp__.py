# -*- coding: utf-8 -*-
# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Picking Mrp Production Inspection",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "mrp",
        "stock",
        "quality_control",
        "quality_control_mrp",
        "quality_control_stock",
        "sale_packaging_info"
    ],
    "data": [
        "views/mrp_production_views.xml",
        "views/qc_inspection_views.xml",
        "views/stock_picking_views.xml",
        "report/certif_analisis_cola_etiq_report.xml",
    ],
    "installable": True,
}
