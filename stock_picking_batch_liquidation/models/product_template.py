# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    liquidation_type = fields.Selection(
        string="Type",
        selection=[("charge", "Charge"), ("pay", "Pay"), ("variable", "Variable")],
    )
    obligatory = fields.Boolean(string="Obligatory")
    price_type = fields.Selection(
        selection=[
            ("correction", "F. M. Correction"),
            ("feed", "Feep"),
            ("average", "Average"),
            ("contract", "Contract"),
        ]
    )
    quantity_type = fields.Selection(
        selection=[("unit", "Unit"), ("kg", "Kg"), ("fixed", "Fixed")]
    )
