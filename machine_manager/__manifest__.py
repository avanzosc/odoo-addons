# -*- coding: utf-8 -*-
# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# Copyright 2015 Daniel Campos - AvanzOSC
# Copyright 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Machine Manager",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "OdooMRP team, "
              "AvanzOSC, "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "contributors": [
        "Daniel Campos <danielcampos@avanzosc.es>",
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
        "Ana Juaristi <ajuaristio@gmail.com>",
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "website": "http://avanzosc.com",
    "depends": [
        "stock",
        "account",
        "product_manufacturer",
        "product",
    ],
    "demo": [
        "demo/machine_model_demo.xml",
        "demo/machinery_user_demo.xml",
        "demo/machinery_demo.xml",
    ],
    "category": "Machinery Management",
    "data": [
        "views/machinery_view.xml",
        "views/machine_model_view.xml",
        "views/machinery_users_view.xml",
        "views/product_view.xml",
        "security/machinery_security.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
