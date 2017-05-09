# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    invoice_by_partner = fields.Boolean(
        string='Invoice analytic lines by partner')

    @api.multi
    def set_parameters(self):
        config_pool = self.env['ir.config_parameter']
        if self.invoice_by_partner:
            config_pool.set_param('invoice_by_partner',
                                  self.invoice_by_partner)
        else:
            # remove the key from parameter
            ids = config_pool.search([('key', '=', 'invoice_by_partner')],)
            if ids:
                ids.unlink()

    @api.model
    def default_get(self, fields):
        res = super(AccountConfigSettings, self).default_get(fields)
        config_pool = self.env['ir.config_parameter']
        res['invoice_by_partner'] = config_pool.get_param(
            'invoice_by_partner', False)
        return res
