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

    def put_in_sale_order_additional_material(self):
        for event in self.filtered(lambda x: x.registration_ids):
            event.registration_ids.put_in_sale_order_additional_material()
