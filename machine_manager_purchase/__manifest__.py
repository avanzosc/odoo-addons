# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# Copyright 2015 Daniel Campos - AvanzOSC
# Copyright 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Machine Manager Purchase",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "OdooMRP team, " "AvanzOSC, " "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "contributors": [
        "Daniel Campos <danielcampos@avanzosc.es>",
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
        "Ana Juaristi <ajuaristio@gmail.com>",
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase_stock",
        "machine_manager",
    ],
    "category": "Machinery Management",
    "data": [
        "views/machine_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
