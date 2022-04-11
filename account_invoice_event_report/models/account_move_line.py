# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class AccountMoveLline(models.Model):
    _inherit = 'account.move.line'

    sale_order_line_id = fields.Many2one(
        string='Sale order line', store=True, comodel_name='sale.order.line',
        compute='_compute_sale_order_line_id')
    event_id = fields.Many2one(
        string='Event', store=True, comodel_name='event.event',
        compute='_compute_event_id')
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
        for line in self.filtered(
                lambda x: x.sale_order_line_id and not x.contract_line_id):
            sale_line = line.sale_order_line_id
            cond = [('event_id', '=', sale_line.event_id.id),
                    ('event_ticket_id', '=', sale_line.event_ticket_id.id),
                    ('sale_order_line_id', '=', sale_line.id)]
            registration = self.env['event.registration'].search(cond)
            if not registration:
                sale = line.sale_order_line_id.order_id
                my_line = sale.order_line.filtered(
                    lambda x: x.event_id.id == sale_line.event_id.id and
                    x.event_ticket_id)
                if my_line and len(my_line) == 1:
                    cond = [('event_id', '=', my_line.event_id.id),
                            ('event_ticket_id', '=',
                             my_line.event_ticket_id.id),
                            ('sale_order_line_id', '=', my_line.id)]
                    registration = self.env['event.registration'].search(cond)
            if len(registration) == 1 and registration.student_id:
                line.student_name = registration.student_id.name
            if len(registration) > 1:
                students_name = ""
                for reg in registration.filtered(lambda x: x.student_id):
                    students_name = (
                        reg.student_id.name if not students_name else
                        "{}, {}".format(students_name, reg.student_id.name))
                line.student_name = students_name
            if not registration:
                line.student_name = ""

    @api.depends('contract_line_id', 'contract_line_id.sale_order_line_id',
                 'sale_line_ids')
    def _compute_sale_order_line_id(self):
        for line in self.filtered(
            lambda x: x.contract_line_id and
                x.contract_line_id.sale_order_line_id):
            sale_line = line.contract_line_id.sale_order_line_id
            line.sale_order_line_id = sale_line.id
        for line in self.filtered(
                lambda x: not x.contract_line_id and x.sale_line_ids):
            if len(line.sale_line_ids) == 1:
                line.sale_order_line_id = line.sale_line_ids[0].id

    @api.depends('sale_order_line_id', 'sale_order_line_id.event_id',
                 'sale_line_ids', 'sale_line_ids.event_id')
    def _compute_event_id(self):
        for line in self.filtered(
            lambda x: x.contract_line_id and x.sale_order_line_id and
                x.sale_order_line_id.event_id):
            line.event_id = line.sale_order_line_id.event_id.id
        for line in self.filtered(
                lambda x: not x.contract_line_id and x.sale_line_ids):
            if (len(line.sale_line_ids) == 1 and
                    line.sale_line_ids[0].event_id):
                line.event_id = line.sale_line_ids[0].event_id.id
