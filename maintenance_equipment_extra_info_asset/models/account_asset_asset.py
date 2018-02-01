# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    invoice_line_id = fields.Many2one(
        comodel_name='account.invoice.line', string='Invoice line')

    @api.model
    def create(self, vals):
        if self.env.context.get('invoice_line_id', False):
            vals['invoice_line_id'] = self.env.context.get('invoice_line_id')
        return super(AccountAssetAsset, self).create(vals)
