# -*- coding: utf-8 -*-
# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class Machine(models.Model):
    _inherit = "machine"

    deprecperc = fields.Float(
        string="Depreciation in %", digits=(10, 2), default=0.0
    )
    deprecperiod = fields.Selection(
        string="Depr. period",
        selection=[("monthly", "Monthly"),
                   ("quarterly", "Quarterly"),
                   ("halfyearly", "Half Yearly"),
                   ("annual", "Yearly")],
        default="annual", required=True
    )
