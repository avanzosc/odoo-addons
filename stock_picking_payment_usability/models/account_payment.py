# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    picking_id = fields.Many2one(string="Picking", comodel_name="stock.picking")
