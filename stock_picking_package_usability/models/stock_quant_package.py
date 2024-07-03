# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    picking_id = fields.Many2one(string="Transfer", comodel_name="stock.picking")
    max_weight = fields.Float(
        string="Maximum Weight", related="product_packaging_id.max_weight", store=True
    )
    pack_length = fields.Float()
    width = fields.Float(string="Pack Width")
    height = fields.Float(string="Pack Height")
    partner_id = fields.Many2one(
        string="Delivery Address",
        comodel_name="res.partner",
        related="picking_id.partner_id",
        store=True,
    )

    @api.onchange("product_packaging_id")
    def onchange_dimension(self):
        if self.product_packaging_id.height:
            self.height = self.product_packaging_id.height
        if self.product_packaging_id.width:
            self.width = self.product_packaging_id.width
        if self.product_packaging_id.packaging_length:
            self.pack_length = self.product_packaging_id.packaging_length
        if self.product_packaging_id.length_uom_id:
            self.length_uom_id = self.product_packaging_id.length_uom_id.id
        if self.product_packaging_id.volume_uom_id:
            self.volume_uom_id = self.product_packaging_id.volume_uom_id.id
        if self.product_packaging_id.weight_uom_id:
            self.weight_uom_id = self.product_packaging_id.weight_uom_id.id
        if self.product_packaging_id.volume:
            self.volume = self.product_packaging_id.volume

    @api.model
    def create(self, vals):
        line = super().create(vals)
        line.name = "{} {} {:0>3}".format(
            line.picking_id.name, "-", len(line.picking_id.quant_package_ids)
        )
        return line
