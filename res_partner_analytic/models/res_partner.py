# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, values):
        partner = super(ResPartner, self).create(values)
        partner._create_analytic_default()
        return partner

    @api.multi
    def _create_analytic_default(self):
        for partner in self.filtered(lambda x: x.is_company and x.customer):
            account = self.env['account.analytic.account'].create({
                'partner_id': partner.id,
                'name': partner.name,
                'type': 'normal',
                'parent_id': self.env.ref(
                    'res_partner_analytic.customer_analytic_account').id,
            })
            self.env['account.analytic.default'].create({
                'company_id': self.env.user.company_id.id,
                'analytic_id': account.id,
                'partner_id': partner.id,
            })
