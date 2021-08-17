# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventAdditionalMaterial(models.Model):
    _name = 'event.additional.material'
    _description = 'Additional material for event'

    event_id = fields.Many2one(
        string='Event', comodel_name='event.event')
    product_id = fields.Many2one(
        string='Product', comodel_name='product.product')
    product_uom_qty = fields.Float(
        string='Quantity', digits='Product Unit of Measure', default=1.0)
    price_unit = fields.Float(
        string='Unit Price', digits='Product Price', default=0.0)

    @api.onchange("product_id")
    def onchange_product_id(self):
        for additional_material in self.filtered(lambda x: x.product_id):
            additional_material.price_unit = (
                additional_material.product_id.lst_price)
