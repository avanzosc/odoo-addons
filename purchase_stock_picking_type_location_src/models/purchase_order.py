# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_picking(self):
        result = super(PurchaseOrder, self)._prepare_picking()
        if self.picking_type_id.default_location_src_id:
            result["location_id"] = self.picking_type_id.default_location_src_id.id
        return result
