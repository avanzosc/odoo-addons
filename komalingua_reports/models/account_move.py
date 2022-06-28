# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    print_with_logo = fields.Boolean(
        string='Print with logo', default=False)
    print_with_3kings_logo = fields.Boolean(
        string='Print with 3Kings logo', default=False)
    print_students = fields.Boolean(
        string='Print students', default=True)
    events = fields.Text(
        string='Events', store=True, compute='_compute_events')

    @api.depends('line_ids', 'line_ids.event_id')
    def _compute_events(self):
        event_obj = self.env['event.event']
        for invoice in self:
            events = event_obj
            for line in invoice.line_ids:
                if line.event_id and line.event_id not in events:
                    events += line.event_id
            name = ''
            if events:
                cond = [('id', 'in', events.ids)]
                my_events = event_obj.with_context(
                    lang=self.env.user.lang).search(cond, order = 'name asc')
                for event in my_events:
                    if not name:
                        name = event.name
                    else:
                        name = u'{}\n{}'.format(event.name, name)
            invoice.events = name

    def put_event_to_transport(self):
        line_obj = self.env['account.move.line']
        for invoice in self:
            lines = invoice.line_ids.filtered(
                lambda x: not x.event_id and x.product_id)
            for line in lines:
                cond = [('move_id', '=', line.move_id.id),
                        ('id', '=', line.id -1)]
                previous_line = line_obj.search(cond, limit=1)
                if (previous_line and previous_line.event_id and
                        previous_line.event_id.displacement_product_ids):
                    displacement_products = (
                        previous_line.event_id.displacement_product_ids)
                    found = displacement_products.filtered(
                        lambda x: x.product_id == line.product_id)
                    if found:
                        line.event_id = previous_line.event_id.id
