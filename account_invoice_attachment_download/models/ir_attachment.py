# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.multi
    @api.depends('res_model', 'res_id')
    def _compute_invoice_info(self):
        invoice_obj = self.env['account.invoice']
        for attachment in self.filtered(
            lambda x: x.res_model and x.res_id and
                x.res_model == 'account.invoice'):
            invoice = invoice_obj.browse(attachment.res_id)
            attachment.invoice_type = invoice.type
            attachment.invoice_date = invoice.date_invoice

    invoice_type = fields.Char(
        'Invoice type', compute='_compute_invoice_info', store=True)
    invoice_date = fields.Date(
        'Invoice date', compute='_compute_invoice_info', store=True)
