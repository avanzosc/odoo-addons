# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    batch_id = fields.Many2one(string="Batch", comodel_name="stock.picking.batch")
    invoicing_qty = fields.Float(string="Total to Invoice")
