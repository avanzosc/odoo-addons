# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ThresholdPercentageBetweenCosts(models.Model):
    _name = "threshold.percentage.between.costs"
    _description = "Threshold percentage between costs"

    name = fields.Char(string="description", required=True)
    threshold_percentage = fields.Float(
        string="Threshold (in %)", digits=(16, 2), default=0.0
    )
