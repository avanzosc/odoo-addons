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
        if self.saca_line_id and self.saca_line_id.estimate_burden:
            self.product_qty = (
                self.saca_line_id.estimate_burden * (
                    self.saca_line_id.estimate_weight))
        return result

    def write(self, values):
        result = super(PurchaseOrderLine, self).write(values)
        if "product_qty" in values:
            for line in self:
                if line.saca_line_id and line.saca_line_id.sale_order_line_ids:
                    line.saca_line_id.sale_order_line_ids[0].product_uom_qty = values["product_qty"]
        if "price_unit" in values:
            for line in self:
                if line.saca_line_id and line.saca_line_id.sale_order_line_ids:
                    line.saca_line_id.sale_order_line_ids[0].price_unit = (
                        values["price_unit"])
        return result