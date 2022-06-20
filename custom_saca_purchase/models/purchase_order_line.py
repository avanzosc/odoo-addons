# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    saca_id = fields.Many2one(
        string="Saca",
        comodel_name="saca",
        related="saca_line_id.saca_id",
        store=True)
    saca_line_id = fields.Many2one(
        string="Saca Line",
        comodel_name="saca.line")
    farm_id = fields.Many2one(
        string="Farm",
        comodel_name="res.partner",
        related="saca_line_id.farm_id",
        store=True)
    farmer_id = fields.Many2one(
        string="Farmer",
        comodel_name="res.partner",
        related="saca_line_id.farmer_id",
        store=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = super(PurchaseOrderLine, self).onchange_product_id()
        if self.saca_line_id and self.saca_line_id.max_weight:
            self.product_qty = self.saca_line_id.max_weight
        return result
