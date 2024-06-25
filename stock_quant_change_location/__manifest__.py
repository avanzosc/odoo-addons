# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Quant Change Location",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "http://www.avanzosc.es",
    "depends": ["stock", "pickings_import_wizard"],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_quant_view.xml",
        "wizard/stock_quant_change_location_wizard_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
