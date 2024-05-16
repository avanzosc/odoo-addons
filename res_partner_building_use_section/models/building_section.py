# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class BuildingSection(models.Model):
    _name = "building.section"
    _description = "Building Section/Area"

    name = fields.Char(
        string="Description",
        required=True,
        copy=False,
    )
    risk = fields.Char(
        copy=False,
    )
    section_use = fields.Many2one(
        comodel_name="building.use",
    )
    superficie = fields.Float(
        string="Surface",
        default=0.0,
        copy=False,
    )
    partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=True,
        copy=False,
    )
    evacuation_height = fields.Float()
