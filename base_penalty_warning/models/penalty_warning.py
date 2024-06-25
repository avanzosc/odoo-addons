# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PenaltyWarning(models.Model):
    _name = "penalty.warning"
    _description = "Penalty warnings"
    _order = "name asc"

    name = fields.Char(string="Name", required=True, copy=False)
    description = fields.Char(string="Description", copy=False)
