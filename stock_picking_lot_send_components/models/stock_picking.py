# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_change_location_production_serial(self):
        for picking in self:
            for line in picking.move_line_ids_without_package:
                if (
                    line.product_id
                    and (line.product_id.tracking) == "serial"
                    and (line.lot_id)
                ):
                    production = self.env["mrp.production"].search(
                        [
                            ("lot_producing_id", "=", line.lot_id.id),
                            ("product_id", "=", line.product_id.id),
                            ("company_id", "=", line.company_id.id),
                        ]
                    )
                    if len(production) > 1:
                        raise ValidationError(
                            _(
                                "This lot {} has been produced in more "
                                + "than one production order."
                            ).format(line.product_id.name)
                        )
                    if len(production) == 1:
                        for component in production.move_line_raw_ids:
                            if component.product_id.tracking == "serial":
                                quant = self.env["stock.quant"].search(
                                    [
                                        ("lot_id", "=", component.lot_id.id),
                                        ("location_usage", "=", "production"),
                                    ]
                                )
                                if quant and len(quant) == 1:
                                    move = self.env["stock.move"].create(
                                        {
                                            "product_id": quant.product_id.id,
                                            "product_uom": (quant.product_id.uom_id.id),
                                            "quantity_done": quant.quantity,
                                            "name": quant.product_id.name,
                                            "location_id": quant.location_id.id,
                                            "location_dest_id": (
                                                line.location_dest_id.id
                                            ),
                                            "company_id": line.company_id.id,
                                        }
                                    )
                                    moveline = move._get_move_lines()
                                    moveline.lot_id = quant.lot_id.id
                                    move._quantity_done_set()
                                    move._action_confirm()
                                    move._action_assign()
                                    move._action_done()
