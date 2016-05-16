# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    def _find_procurements_from_stock_information(
        self, company, to_date, states=None, from_date=None, category=None,
            template=None, products=None, location_id=None,
            without_reserves=True, without_plan=True):
        procurements = super(
            ProcurementOrder, self)._find_procurements_from_stock_information(
            company, to_date, states=states, from_date=from_date,
            category=category, template=template, products=products,
            location_id=location_id)
        if without_reserves:
            procurements = procurements.filtered(lambda x: not x.reservation)
        else:
            procurements = procurements.filtered(lambda x: x.reservation)
        if without_plan:
            procurements = procurements.filtered(lambda x: not x.plan)
        else:
            procurements = procurements.filtered(lambda x: x.plan)
        return procurements
