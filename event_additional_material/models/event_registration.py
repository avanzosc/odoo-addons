# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_confirm(self):
        result = super(EventRegistration, self).action_confirm()
        self.put_in_sale_order_additional_material()
        return result

    def put_in_sale_order_additional_material(self):
        for registration in self.filtered(
                lambda x: x.event_id.add_mat_automatically and
                x.sale_order_id):
            event = registration.event_id
            for additional_material in event.additional_material_ids:
                line = registration.sale_order_id.order_line.filtered(
                    lambda a: a.product_id == additional_material.product_id)
                if not line:
                    registration.create_sale_line_with_additional_material(
                        registration.sale_order_id,
                        additional_material)
                else:
                    registration.update_sale_line_from_additional_material(
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
        num_registrations = len(self.event_id.registration_ids.filtered(
            lambda x: x.state == 'open' and x.sale_order_id
            and x.sale_order_id == self.sale_order_id))
        return (material.product_uom_qty * num_registrations
                if num_registrations else 0)

    @api.model_create_multi
    def create(self, vals_list):
        if 'from_material_module' not in self.env.context:
            return super(EventRegistration, self).create(vals_list)
        my_vals = []
        if isinstance(vals_list, dict):
            my_vals = vals_list
            sale_line = self.catch_sale_line_from_create_registration(
                vals_list)
            if sale_line and not sale_line.event_ticket_id:
                my_vals = {}
        else:
            for val in vals_list:
                sale_line = self.catch_sale_line_from_create_registration(val)
                if sale_line and sale_line.event_ticket_id:
                    my_vals.append(val)
        return super(EventRegistration, self).create(my_vals)

    def catch_sale_line_from_create_registration(self, vals):
        sale_line_obj = self.env['sale.order.line']
        if ('sale_order_line_id' in vals and
                vals.get('sale_order_line_id', False)):
            return sale_line_obj.browse(vals.get('sale_order_line_id'))
        return sale_line_obj
