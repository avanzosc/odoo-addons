# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    shipping_method_id = fields.Many2one(
        string='Shipping Method',
        comodel_name='delivery.carrier')
    transporter_id = fields.Many2one(
        string='Transporter',
        comodel_name='res.partner',
        related='shipping_method_id.partner_id',
        store=True)
    shipping_cost = fields.Float(string='Shipping Cost')

    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        for order in self:
            order.picking_ids.write(
                {'shipping_method_id': order.shipping_method_id.id,
                 'shipping_cost': order.shipping_cost})
        return result
