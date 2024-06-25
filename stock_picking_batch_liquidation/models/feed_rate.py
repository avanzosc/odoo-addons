# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class FeedRate(models.Model):
    _name = "feed.rate"
    _description = "Feep Rate"

    feed = fields.Integer(string="Feep")
    price = fields.Float(string="Price", digits="Feep Decimal Precision")
    contract_id = fields.Many2one(
        string="Contract", comodel_name="liquidation.contract"
    )
