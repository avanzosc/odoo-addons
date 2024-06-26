# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_picking(self):
        values = super()._prepare_picking()
        if self.dest_address_id:
            values["owner_id"] = self.dest_address_id.id
        return values
