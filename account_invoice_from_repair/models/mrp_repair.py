# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    @api.multi
    def action_invoice_create(self, group=False):
        res = super(MrpRepair, self).action_invoice_create(group=group)
        invoice_obj = self.env['account.invoice']
        for repair in self:
            invoice = invoice_obj.browse(res[repair.id])
            invoice.payment_mode_id = repair.partner_id.customer_payment_mode
            invoice.partner_bank_id = (
                repair.partner_id.customer_payment_mode.bank_id)
            invoice.payment_term = repair.partner_id.property_payment_term
        return res
