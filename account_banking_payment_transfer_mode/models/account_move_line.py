# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    @api.depends('stored_invoice_id', 'stored_invoice_id.payment_mode_id',
                 'manual_payment_mode')
    @api.multi
    def _compute_payment_mode(self):
        for record in self:
            record.payment_mode_id = \
                record.stored_invoice_id.payment_mode_id.id if \
                record.stored_invoice_id else record.manual_payment_mode.id

    manual_payment_mode = fields.Many2one(
        comodel_name='payment.mode', string='Manual Payment Mode')
    payment_mode_id = fields.Many2one(
        comodel_name='payment.mode', string='Payment Mode',
        compute='_compute_payment_mode', store=True, related=False)
