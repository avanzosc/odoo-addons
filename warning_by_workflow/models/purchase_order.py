# -*- coding: utf-8 -*-
# Copytight 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.multi
    def purchase_confirm(self):
        for order in self:
            if not self.env.context.get('bypass_warning', False):
                types = []
                if order.has_stockable_product():
                    types += ['picking_warn']
                if order.invoice_method == 'order':
                    types += ['invoice_warn']
                return order.partner_id.get_partner_warning(types, order,
                                                            'purchase_confirm')
            res = order.signal_workflow('purchase_confirm')
        return res
