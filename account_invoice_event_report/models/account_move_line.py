# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class AccountMoveLline(models.Model):
    _inherit = 'account.move.line'

    sale_order_line_id = fields.Many2one(
        string='Sale order line', store=True, comodel_name='sale.order.line',
        related='contract_line_id.sale_order_line_id')
    event_id = fields.Many2one(
        string='Event', store=True, comodel_name='event.event',
        related='sale_order_line_id.event_id')
    student_name = fields.Char(
        string='Student name', compute='_compute_student_name')

    def _compute_student_name(self):
        for line in self.filtered(
                lambda x: x.sale_order_line_id and x.contract_line_id):
            cond = [('sale_order_line_id', '=', line.sale_order_line_id.id),
                    ('contract_line_id', '=', line.contract_line_id.id)]
            registration = self.env['event.registration'].search(cond, limit=1)
            if registration and registration.student_id:
                line.student_name = registration.student_id.name
