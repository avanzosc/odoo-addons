# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class WizCatchOldSaleOrder(models.TransientModel):
    _name = 'wiz.catch.old.sale.order'
    _description = 'Wizard for catch old sale order'

    @api.multi
    def update_old_sale_order(self):
        account_obj = self.env['account.analytic.account']
        sale_obj = self.env['sale.order']
        cond = [('name', 'ilike', '%2017%')]
        accounts = account_obj.search(cond)
        cond = [('project_id', 'in', accounts.ids),
                ('old_sale_order_id', '=', False)]
        sales = sale_obj.search(cond)
        for sale in sales:
            name = sale.project_id.name.replace(' 2017', '')
            cond = [('name', '=', name)]
            account = account_obj.search(cond, limit=1)
            sale.old_sale_order_id = account.sale.id
