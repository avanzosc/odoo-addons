# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class Frame(models.Model):
    _name = "frame"
    _description = "Frame"

    name = fields.Char()
    workcenter_id = fields.Many2one(
        string="Workcenter",
        comodel_name="mrp.workcenter",
    )
    width = fields.Float()
    step = fields.Float()
    description = fields.Char()
