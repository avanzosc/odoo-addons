# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    invoice_line_id = fields.Many2one(
        comodel_name='account.invoice.line', string='Invoice line')
