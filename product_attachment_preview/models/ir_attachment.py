# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def _get_default_is_technical(self):
        if self.env.user.has_group(
            "product_attachment_preview.group_tech_ope_product_attachment_only"
        ):
            return True
        return False

    is_technical = fields.Boolean(
        string="Technicians", default=_get_default_is_technical
    )
    is_for_operators = fields.Boolean(string="Operators", default=False)
