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
    def _onchange_tractor_id(self):
        for partner in self:
            if partner.tractor_id and partner.tractor_id.driver_id:
                partner.driver_id = partner.tractor_id.driver_id.id
