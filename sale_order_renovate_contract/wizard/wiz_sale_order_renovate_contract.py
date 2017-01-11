# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class WizSaleOrderRenovateContract(models.TransientModel):
    _name = 'wiz.sale.order.renovate.contract'
    _description = 'Wizard for renovate sale and contract'

    @api.multi
    def renovate_sale_order_and_contract(self):
        self._search_sales()._renovate_sale_and_contract_from_wizard()

    def _search_sales(self):
        sales = self.env['sale.order'].browse(
            self.env.context.get('active_ids')).filtered(
            lambda x: x.project_id and x.project_id.date)
        return sales
