# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _find_productions_from_stock_information(
        self, company, to_date, product, location, state=None,
            from_date=None):
        cond = [('company_id', '=', company.id),
                ('product_id', '=', product.id),
                ('date_planned', '<=', to_date),
                ('location_dest_id', '=', location.id)]
        if state:
            cond.append(('state', 'in', state))
        if from_date:
            cond.append(('date_planned', '>=', from_date))
        productions = self.search(cond)
        return productions
