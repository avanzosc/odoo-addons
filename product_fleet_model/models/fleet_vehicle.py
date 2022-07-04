# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.tag_ids = self.product_id.tag_ids
            self.model_id = self.product_id.model_id
