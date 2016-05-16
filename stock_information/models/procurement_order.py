# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    def _find_procurements_from_stock_information(
        self, company, to_date, states=None, from_date=None, category=None,
            template=None, products=None, location_id=None):
        cond = [('company_id', '=', company.id),
                ('date_planned', '<=', to_date)]
        if states:
            cond.append(('state', 'in', states))
        else:
            cond.append(('state', 'not in', ('cancel', 'done')))
        if from_date:
            cond.append(('date_planned', '>=', from_date))
        if products:
            cond.append(('product_id', 'in', products))
        if location_id:
            cond.append(('location_id', '=', location_id.id))
        procurements = self.search(cond)
        procurements = procurements.filtered(
            lambda x: x.location_id.usage == 'internal')
        if category:
            procurements = procurements.filtered(
                lambda x: x.product_id.product_tmpl_id.categ_id.id ==
                category.id)
        if template:
            procurements = procurements.filtered(
                lambda x: x.product_id.product_tmpl_id.id ==
                template.id)
        return procurements
