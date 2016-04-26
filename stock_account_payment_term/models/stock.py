# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        inv_vals = super(StockPicking, self)._get_invoice_vals(
            key, inv_type, journal_id, move)
        res = self.env['account.invoice'].onchange_payment_term_date_invoice(
            inv_vals['payment_term'], inv_vals['date_invoice'] or
            fields.Date.context_today(self))
        inv_vals['date_due'] = res['value']['date_due']
        return inv_vals
