# -*- coding: utf-8 -*-
# Copytight 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def launch_create_invoice(self):
        self.ensure_one()
        if not self.env.context.get('bypass_warning', False):
            return self.partner_id.get_partner_warning(
                ['invoice_warn'], self, 'launch_create_invoice')
        action = self.env.ref('stock_account.action_stock_invoice_onshipping')
        action = action.read()[0]
        return action
