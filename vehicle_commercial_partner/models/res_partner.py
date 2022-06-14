# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vehicle_ids = fields.One2many(
        string="Vehicles",
        comodel_name="fleet.vehicle",
        inverse_name="commercial_partner_id")
