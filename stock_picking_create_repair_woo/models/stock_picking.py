# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_confirm(self):
        self._check_company()
        for picking in self.filtered(
            lambda x: x.is_repair and x.picking_type_id.code == "incoming"
        ):
            has_generic = any(
                picking.move_ids_without_package.mapped(
                    "product_id.generic_repair_product"
                )
            )
            if has_generic:
                error = _(
                    "This operation is not allowed because picking contains"
                    " a generic repair product."
                )
                raise ValidationError(error)
        return super().action_confirm()
