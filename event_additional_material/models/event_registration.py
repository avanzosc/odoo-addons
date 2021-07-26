# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_confirm(self):
        result = super(EventRegistration, self).action_confirm()
        for registration in self.filtered(
                lambda x: x.event_id.add_mat_automatically and
                x.sale_order_id):
            registration.event_id.put_in_sale_order_additional_material(
                registration.sale_order_id)
        return result
