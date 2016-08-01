# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        for order in self:
            groupings = order.mapped(
                'order_line.product_id.categ_id.procured_purchase_grouping')
            try:
                groupings |= order.mapped(
                    'order_line.product_tmpl_id.categ_id.'
                    'procured_purchase_grouping')
            except:
                pass
            check_project = False
            for grouping in groupings:
                check_project = grouping == 'sale_contract'
                if check_project:
                    break
            if check_project and not order.project_id:
                raise exceptions.Warning(
                    _('You must enter the project/contract'))
        return super(SaleOrder, self).action_button_confirm()
