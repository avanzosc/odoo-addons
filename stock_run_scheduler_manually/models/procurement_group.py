# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api
from odoo.osv import expression


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    def _get_orderpoint_domain(self, company_id=False):
        domain = [('company_id', '=', company_id)] if company_id else []
        domain += [('product_id.active', '=', True)]
        if 'my_orderpoint_id' in self.env.context:
            domain.append(
                ('id', '=', self.env.context.get('my_orderpoint_id')))
        return domain

    @api.model
    def _get_moves_to_assign_domain(self, company_id):
        domain = super(ProcurementGroup, self)._get_moves_to_assign_domain(
            company_id)
        domain = expression.AND(
            [domain, [('product_id', '=',
                       self.env.context.get('my_product_id'))]])
        return domain
