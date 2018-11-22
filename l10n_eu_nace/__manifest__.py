# Copyright 2011 Numérigraphe SARL.
# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "European NACE Activities",
    "version": "11.0.1.0.0",
    "author": "Numérigraphe SARL, "
              "Sistheo, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "category": "Localisation/Europe",
    "depends": [
        "contacts",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/res_partner_nace_view.xml",
        "wizard/nace_import_view.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
