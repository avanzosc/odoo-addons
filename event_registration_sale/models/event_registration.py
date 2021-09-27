# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    partner_bank_acc_id = fields.Many2one(
        string='Partner bank account',
        comodel_name='res.partner.bank',
        store=True,
        compute='_compute_event_partner_bank_acc')
    order_status = fields.Selection(
        string='Order status', store=True,
        related='sale_order_id.state')
    event_ticket_product_id = fields.Many2one(
        string='Event ticket product', comodel_name='product.product',
        related='event_ticket_id.product_id', store=True)
    event_ticket_price = fields.Float(
        string='Event ticket price', digits=dp.get_precision('Product Price'),
        related='event_ticket_id.price', store=True)
    sale_line_product_id = fields.Many2one(
        string='Sale line product', comodel_name='product.product',
        related='sale_order_line_id.product_id', store=True)
    sale_line_price = fields.Float(
        string='Sale line price', digits=dp.get_precision('Product Price'),
        related='sale_order_line_id.price_unit', store=True)
    with_distinct_product = fields.Boolean(
        string='With distinct product', store=True,
        compute='_compute_with_distinct_product')
    with_distinct_price = fields.Boolean(
        string='With distinct price', store=True,
        compute='_compute_with_distinct_price')

    @api.depends('event_ticket_product_id', 'sale_line_product_id')
    def _compute_with_distinct_product(self):
        for record in self:
            distinct = False
            if (record.event_ticket_product_id and
                record.sale_line_product_id and
                record.event_ticket_product_id !=
                    record.sale_line_product_id):
                distinct = True
            if record.with_distinct_price != distinct:
                record.with_distinct_price = distinct

    @api.depends('event_ticket_price', 'sale_line_price')
    def _compute_with_distinct_price(self):
        for record in self:
            distinct = False
            if (record.event_ticket_price and record.sale_line_price and
                    record.event_ticket_price != record.sale_line_price):
                distinct = True
            if record.with_distinct_product != distinct:
                record.with_distinct_product = distinct

    @api.depends('partner_id',
                 'partner_id.bank_ids')
    def _compute_event_partner_bank_acc(self):
        for record in self:
            record.partner_bank_acc_id = self.env['res.partner.bank'].search(
                [('id', 'in', record.partner_id.bank_ids.ids)],
                order='id desc', limit=1)

    def action_confirm(self):
        for reg in self.filtered(lambda x: x.sale_order_line_id):
            line = reg.sale_order_line_id
            if line.product_id != reg.event_ticket_product_id:
                line.product_id = reg.event_ticket_product_id.id
                line.product_id_change()
            if line.price_unit != reg.event_ticket_price:
                line.price_unit = reg.event_ticket_price
                line._onchange_discount()
        return super(EventRegistration, self).action_confirm()
