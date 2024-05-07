# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    license_plate = fields.Char(string="License Plate")

    @api.onchange("license_plate")
    def _onchange_license_plate(self):
        if self.license_plate:
            for picking in self.picking_ids:
                picking.license_plate = self.license_plate
