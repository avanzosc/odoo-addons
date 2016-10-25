# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        plan_obj = self.env['procurement.plan']
        res = super(SaleOrder, self).action_button_confirm()
        for sale in self:
            cond = [('name', 'ilike', sale.name)]
            plan = plan_obj.search(cond, limit=1)
            if plan:
                plan._update_stock_information()
        return res
