# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    batch_id = fields.Many2one(string="Batch", comodel_name="stock.picking.batch")

    @api.model
    def create(self, vals):
        line = super().create(vals)
        if line.batch_id:
            line.name = "{} {} {:0>3}".format(
                line.batch_id.name, "-", len(line.batch_id.quant_package_ids)
            )
        return line
