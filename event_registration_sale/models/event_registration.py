
from odoo import models, fields, api


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    partner_bank_acc_id = fields.Many2one(
        string='Partner bank account',
        comodel_name='res.partner.bank',
        store=True,
        compute='_compute_event_partner_bank_acc')
    order_status = fields.Selection(
        string='Order status',
        related='sale_order_id.state')

    @api.depends('partner_id',
                 'partner_id.bank_ids')
    def _compute_event_partner_bank_acc(self):
        for record in self:
            record.partner_bank_acc_id = self.env['res.partner.bank'].search(
                [('id', 'in', record.partner_id.bank_ids.ids)],
                order='id desc', limit=1)
