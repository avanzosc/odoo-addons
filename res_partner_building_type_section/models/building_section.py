# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class BuildingSection(models.Model):
    _name = "building.section"
    _description = "Building Section/Area"

    name = fields.Char(string="Description", required=True, copy=False)
    risk_use = fields.Char(string="Risk/User", copy=False)
    superficie = fields.Float(string="Superficie", default=0.0, copy=False)
    partner_id = fields.Many2one(
        string="Contact", comodel_name="res.partner", required=True, copy=False
    )
