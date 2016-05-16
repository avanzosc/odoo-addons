# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "MRP - BoM line structure show child with manual standard cost",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "OdooMRP team,"
              "AvanzOSC,"
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "website": "http://www.odoomrp.com",
    "contributors": [
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
        ],
    "category": "Manufacturing",
    "depends": [
        "mrp_bom_structure_show_child",
        "mrp_production_estimated_cost",
    ],
    "data": [
        "views/mrp_bom_line_structure_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
