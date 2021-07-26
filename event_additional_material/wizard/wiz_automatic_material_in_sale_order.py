# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class WizAutomaticMaterialInSaleOrder(models.TransientModel):
    _name = 'wiz.automatic.material.in.sale.order'
    _description = 'Wizard for put additinal material in sale order.'

    name = fields.Text(string='Description')

    def action_put_material_from_registration(self):
        self.ensure_one()
        registrations = self.env['event.registration'].browse(
            self.env.context.get('active_ids'))
        for registration in registrations.filtered(lambda x: x.sale_order_id):
            registration.event_id.put_in_sale_order_additional_material(
                registration.sale_order_id)
