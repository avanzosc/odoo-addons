# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipping_method_id = fields.Many2one(
        string='Shipping Method',
        comodel_name='delivery.carrier')
    transporter_id = fields.Many2one(
        string='Transporter',
        comodel_name='res.partner',
        related='shipping_method_id.partner_id',
        store=True)
    shipping_cost = fields.Float(string='Shipping Cost')
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id.id)
    license_plate = fields.Char(string='Transport License Plate')
