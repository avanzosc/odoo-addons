# -*- coding: utf-8 -*-
# © 2015 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "BOM lines configurator",
    "version": "8.0.1.0.2",
    "license": "AGPL-3",
    "depends": ["product_attribute_code_field",
                "product_variant_default_code",
                "mrp_product_variants",
                "mrp_hook_extension"
    ],
    "author": "OdooMRP team, "
              "AvanzOSC, ",
    "website": "http://www.odoomrp.com",
    "contributors": [
        "Mikel Arregi <mikelarregi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "Manufacturing",
    "data": [
        "data/formula_eval_precision.xml",
        "views/bom_line_view.xml",
        "views/mrp_bom_line_rule_view.xml",
        "views/mrp_bom_line_variant_sector.xml",
        "views/mrp_constant_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
