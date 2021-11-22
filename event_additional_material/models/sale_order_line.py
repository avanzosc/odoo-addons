# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _update_registrations(self, confirm=True, cancel_to_draft=False,
                              registration_data=None, mark_as_paid=False):
        result = super(
            SaleOrderLine, self.with_context(
                from_material_module=True))._update_registrations(
                    confirm=confirm, cancel_to_draft=cancel_to_draft,
                    registration_data=registration_data,
                    mark_as_paid=mark_as_paid)
        return result
