# -*- coding: utf-8 -*-
# Copytight 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        for order in self:
            if not self.env.context.get('bypass_warning', False):
                types = []
                if (order.procurement_needed() and
                        (order.invoiced or order.order_policy != 'prepaid')):
                    types += ['picking_warn']
                if order.order_policy == 'prepaid':
                    types += ['invoice_warn']
                return order.partner_id.get_partner_warning(
                    types, order, 'action_button_confirm')
            else:
                res = super(SaleOrder, self).action_button_confirm()
        return res

    @api.multi
    def launch_create_invoice(self):
        self.ensure_one()
        if not self.env.context.get('bypass_warning', False):
            return self.partner_id.get_partner_warning(
                ['invoice_warn'], self, 'launch_create_invoice')
        action = self.env.ref('sale.action_view_sale_advance_payment_inv')
        action = action.read()[0]
        return action
