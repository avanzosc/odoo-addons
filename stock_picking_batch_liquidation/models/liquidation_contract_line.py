# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class LiquidationContractLine(models.Model):
    _name = "liquidation.contract.line"
    _description = "Liquidation Contract Line"

    product_id = fields.Many2one(
        string="Product", comodel_name="product.product", required=True
    )
    type = fields.Selection(
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
    move_type_id = fields.Many2one(string="Move Type", comodel_name="move.type")
    contract_id = fields.Many2one(
        string="Contract", comodel_name="liquidation.contract"
    )
    price = fields.Float(string="Price")

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.type = self.product_id.liquidation_type
            self.obligatory = self.product_id.obligatory
            self.price_type = self.product_id.price_type
            self.move_type_id = self.product_id.categ_id.move_type_id.id
            self.quantity_type = self.product_id.quantity_type
