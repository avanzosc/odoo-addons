# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class Machine(models.Model):
    _inherit = "machine"

    purch_inv_id = fields.Many2one(
        string="Purchase Invoice", comodel_name="account.move"
    )
