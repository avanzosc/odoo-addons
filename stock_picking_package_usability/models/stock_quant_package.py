# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    picking_id = fields.Many2one(string="Transfer", comodel_name="stock.picking")
    max_weight = fields.Float(
        string="Maximum Weight", related="package_type_id.max_weight", store=True
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

    @api.onchange("packaging_type_id")
    def onchange_dimension(self):
        if self.packaging_type_id.height:
            self.height = self.packaging_type_id.height
        if self.packaging_type_id.width:
            self.width = self.packaging_type_id.width
        if self.packaging_type_id.packaging_length:
            self.pack_length = self.packaging_type_id.packaging_length

    @api.model
    def create(self, vals):
        line = super().create(vals)
        line.name = "{} {} {:0>3}".format(
            line.picking_id.name, "-", len(line.picking_id.quant_package_ids)
        )
        return line
