# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allow_modify_tracking = fields.Boolean(compute="_compute_allow_modify_tracking")

    def _compute_allow_modify_tracking(self):
        for template in self:
            template.allow_modify_tracking = self.env.user.has_group(
                "product_tracking_group.group_product_traceability_manager"
            )
