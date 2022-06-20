# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SacaLineStage(models.Model):
    _name = "saca.line.stage"
    _description = "Saca Line Stage"
    _order = "sequence"

    name = fields.Char(string="Stage")
    sequence = fields.Integer(string="Sequence", copy=False)
    color_name = fields.Selection(
        string="Color",
        selection=[
            ("red", "Red"),
            ("blue", "Blue"),
            ("green", "Green"),
            ("yellow", "Yellow"),
            ("gray", "Gray"),
            ("purple", "Purple")],
        default="gray")
