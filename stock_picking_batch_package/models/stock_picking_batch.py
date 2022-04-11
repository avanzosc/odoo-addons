# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    def set_domain_for_partner_id(self):
        delivery_carrier = self.env['delivery.carrier'].search([(1, '=', 1)])
        partner_list = []
        for record in delivery_carrier:
            if record.partner_id:
                partner_list.append(record.partner_id.id)
        return [('id', 'in', partner_list)]

    partner_id = fields.Many2one(
        string='Transporter',
        comodel_name='res.partner',
        domain=set_domain_for_partner_id)
    number_of_packages = fields.Integer(
        string='Number of Packages',
        compute='_compute_number_of_packages')
    shipping_weight = fields.Float(
        string='Shipping Weight',
        compute='_compute_shipping_weight')

    def _compute_number_of_packages(self):
        for transfer in self:
            transfer.number_of_packages = sum(
                transfer.picking_ids.mapped('number_of_packages'))

    def _compute_shipping_weight(self):
        for transfer in self:
            transfer.shipping_weight = sum(
                transfer.picking_ids.mapped('shipping_weight'))
