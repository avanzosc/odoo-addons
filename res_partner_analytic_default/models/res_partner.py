# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    analytic_default = fields.Many2one(
        'account.analytic.default', string='Default Analytic Account')

    @api.model
    def create(self, values):
        if ('is_company' in values and values.get('is_company') and
                'customer' in values and values.get('customer')):
            values['analytic_default'] = self._create_analytic_default(
                values.get('name')).id
        partner = super(ResPartner, self).create(values)
        if partner.analytic_default:
            partner.analytic_default.partner_id = partner.id
        return partner

    def _create_analytic_default(self, name):
        analytic_vals = {'name': _('Customer: ') + name,
                         'type': 'normal'}
        account = self.env['account.analytic.account'].create(analytic_vals)
        vals = {'company_id': self.env.user.company_id.id,
                'analytic_id': account.id}
        default_account = self.env['account.analytic.default'].create(vals)
        return default_account
