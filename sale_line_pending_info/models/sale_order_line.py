# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.depends('product_uom_qty', 'qty_delivered', 'price_unit')
    def _compute_qty_amount_pending_delivery(self):
        for line in self:
            line.qty_pending_delivery = (
                line.product_uom_qty - line.qty_delivered)
            line.amount_pending_delivery = (
                line.qty_pending_delivery * line.price_unit)

    @api.multi
    @api.depends('product_uom_qty', 'qty_invoiced')
    def _compute_qty_amount_pending_invoicing(self):
        for line in self:
            line.qty_pending_invoicing = (
                line.product_uom_qty - line.qty_invoiced)
            line.amount_pending_invoicing = (
                line.qty_pending_invoicing * line.price_unit)

    qty_pending_delivery = fields.Float(
        string='Pending delivery qty', copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_qty_amount_pending_delivery', store=True)
    amount_pending_delivery = fields.Monetary(
        string='Amount pending delivery', copy=False,
        compute='_compute_qty_amount_pending_delivery', store=True)
    qty_pending_invoicing = fields.Float(
        string='Pending invoicing qty', copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_qty_amount_pending_invoicing', store=True)
    amount_pending_invoicing = fields.Monetary(
        string='Amount pending invoicing', copy=False,
        compute='_compute_qty_amount_pending_invoicing', store=True)
