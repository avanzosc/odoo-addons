# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountConfigSettings(models.TransientModel):

    _inherit = 'account.config.settings'

    unified_risk_default = fields.Boolean(
        string='Unified Risk By Default in Partners')

    @api.multi
    def set_parameters(self):
        config_pool = self.env['ir.config_parameter']
        if self.unified_risk_default:
            config_pool.set_param('unified.risk.default',
                                  self.unified_risk_default)
        else:
            ids = config_pool.search([('key', '=', 'unified.risk.default')])
            ids.unlink()

    @api.model
    def default_get(self, fields):
        res = super(AccountConfigSettings, self).default_get(fields)
        res['unified_risk_default'] = self.env['ir.config_parameter'
                                               ].get_param(
            'unified.risk.default')
        return res

    @api.multi
    def get_unified_risk_default_value(self):
        return self.env['ir.config_parameter'].get_param(
            'unified.risk.default')
