# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    tractor_id = fields.Many2one(
        string="Tractor",
        comodel_name="fleet.vehicle",
    )
    semi_trailer_id = fields.Many2one(
        string="Semi-Trailer",
        comodel_name="fleet.vehicle",
    )

    @api.onchange("tractor_id")
    def onchange_tractor_id(self):
        self.ensure_one()
        if self.tractor_id and self.tractor_id.driver_id:
            self.driver_id = self.tractor_id.driver_id.id
