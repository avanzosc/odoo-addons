# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    carrier_id = fields.Many2one(
        string='Shipping Method')
    transporter_id = fields.Many2one(
        string='Transporter',
        comodel_name='res.partner',
        related='carrier_id.partner_id',
        store=True)
    shipping_cost = fields.Float(
        string='Shipping Cost',
        digits='Shipping Cost Decimal Precision')
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id.id)
    license_plate = fields.Char(string='Transport License Plate')
    total_done_qty = fields.Float(
        string='Total Done Quantity',
        compute='_compute_total_done_qty')
    transport_price = fields.Float(
        string='Transport Price',
        compute='_compute_transport_price')

    def _compute_total_done_qty(self):
        for picking in self:
            picking.total_done_qty = 0
            if picking.move_ids_without_package:
                picking.total_done_qty = sum(
                    picking.move_ids_without_package.mapped('quantity_done'))

    def _compute_transport_price(self):
        for picking in self:
            picking.transport_price = (
                picking.shipping_cost * picking.total_done_qty)

    def action_invoice_trasport_lines(self):
        if self.shipping_cost > 0 and (
            self.carrier_id is not False) and (
                self.state == 'done' and self.transporter_id):
            for line in self.move_ids_without_package:
                cond = [('transfer_id', '=', self.id),
                        ('product_id', '=', line.product_id.id)]
                line_done = (
                    self.env['transport.carrier.lines.to.invoice'].search(
                        cond, limit=1))
                vals = {'transfer_id': self.id,
                        'shipping_method_id': self.carrier_id.id,
                        'transporter_id': self.transporter_id.id,
                        'product_id': self.carrier_id.product_id.id,
                        'product_qty': line.quantity_done,
                        'product_uom_id': line.product_uom.id,
                        'price_unit': self.shipping_cost,
                        'total_price': (
                            self.shipping_cost * line.quantity_done),
                        'date': self.date_done.date(),
                        'description': u'{} {}'.format(
                            self.name, self.date_done.date())}
                if not line_done:
                    self.env['transport.carrier.lines.to.invoice'].create(vals)

    def button_validate(self):
        self.ensure_one()
        result = super(StockPicking, self).button_validate()
        self.action_invoice_trasport_lines()
        return result
