# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            error = []
            for move_line in picking.move_line_ids.filtered(
                lambda ml: ml.product_id.type == "product"
                and ml.location_dest_id.not_allowed_as_destination
            ):
                error.append(
                    _(
                        "The product: %(product_name)s, has the destination "
                        "location: %(destination_name)s, and this location "
                        "is not permitted as a destination location."
                    )
                    % {
                        "product_name": move_line.product_id.name,
                        "destination_name": move_line.location_dest_id.name,
                    }
                )
            if error:
                raise ValidationError("\n".join(error))
        return super().button_validate()
