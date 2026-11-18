# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairService(models.Model):
    _inherit = "repair.service"

    @api.model
    def _get_default_product_id(self):
        cond = [("default_product_manufacturing_operations", "=", True)]
        return self.env["product.product"].search(cond, limit=1)

    product_id = fields.Many2one(default=_get_default_product_id)
