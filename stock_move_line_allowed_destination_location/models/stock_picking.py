# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            for move_line in picking.move_line_ids_without_package:
                if move_line.location_dest_id.not_allow_movelines_at_destination:
                    error = _(
                        "The product: %(product_name)s, has the destination "
                        "location:: %(destination_name)s, and this location "
                        "is not permitted as a destination location."
                    ) % {
                        "product_name": move_line.product_id.name,
                        "destination_name": move_line.location_dest_id.name,
                    }
                    raise ValidationError(error)
        return super().button_validate()
