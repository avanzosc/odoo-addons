# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    add_mat_automatically = fields.Boolean(
        string='Automatically add to sales order',
        help='Insert in sale order additional material automatically when '
        'confirming participant?')
    additional_material_ids = fields.One2many(
        string='Additional materials',
        comodel_name='event.additional.material', inverse_name='event_id')

    def put_in_sale_order_additional_material(self, sale):
        for event in self.filtered(lambda x: x.additional_material_ids):
            for additional_material in event.additional_material_ids:
                line = sale.order_line.filtered(
                    lambda a: a.product_id == additional_material.product_id)
                if not line:
                    event.create_sale_line_with_additional_material(
                        sale, additional_material)
                else:
                    event.update_sale_line_from_additional_material(
                        line, additional_material)

    def create_sale_line_with_additional_material(self, sale, material):
        product_uom_qty = self.calculate_additional_material_qty(material)
        vals = {
            'order_id': sale.id,
            'product_id': material.product_id.id,
            'name': material.product_id.name,
            'product_uom': material.product_id.uom_id.id,
            'product_uom_qty': product_uom_qty,
            'price_unit': 1}
        line = self.env['sale.order.line'].create(vals)
        line.product_id_change()
        line.price_unit = material.price_unit

    def update_sale_line_from_additional_material(self, sale_line, material):
        product_uom_qty = self.calculate_additional_material_qty(material)
        vals = {
            'product_uom_qty': product_uom_qty,
            'price_unit': material.price_unit}
        sale_line.write(vals)

    def calculate_additional_material_qty(self, material):
        num_registrations = len(self.registration_ids.filtered(
            lambda x: x.state == 'open'))
        return material.product_uom_qty * num_registrations
