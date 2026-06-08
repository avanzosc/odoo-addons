# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class Machine(models.Model):
    _inherit = "machine"

    account_asset_id = fields.Many2one(
        string="Asset", comodel_name="account.asset", copy=False
    )
