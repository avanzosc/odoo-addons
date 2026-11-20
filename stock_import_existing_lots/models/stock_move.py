# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends(
        "has_tracking",
        "picking_type_id.use_create_lots",
        "picking_type_id.use_existing_lots",
        "product_id",
    )
    def _compute_display_assign_serial(self):
        result = super()._compute_display_assign_serial()
        for move in self:
            move.display_import_lot = (
                move.has_tracking != "none"
                and move.product_id
                and not move.origin_returned_move_id.id
                and move.state not in ("done", "cancel")
            )
        return result

    @api.model
    def _search_lot_ids_from_move_line_vals(
        self, vals_list, product_id, company_id=False
    ):
        lot_names = {vals["lot_name"] for vals in vals_list if vals.get("lot_name")}
        lots = self.env["stock.lot"].search(
            [
                ("product_id", "=", product_id),
                "|",
                ("company_id", "=", company_id),
                ("company_id", "=", False),
                ("name", "in", list(lot_names)),
            ]
        )
        lot_id_by_name = {lot.name: lot.id for lot in lots}
        missing_names = lot_names - set(lot_id_by_name)
        if missing_names:
            raise UserError(
                _(
                    "The following lots/serial numbers do not exist for this "
                    "product: %s",
                    ", ".join(sorted(missing_names)),
                )
            )
        for vals in vals_list:
            lot_name = vals.get("lot_name")
            if not lot_name:
                continue
            vals["lot_id"] = lot_id_by_name[lot_name]
            vals["lot_name"] = False

    @api.model
    def action_generate_lot_line_vals(  # noqa: C901
        self, context, mode, first_lot, count, lot_text
    ):
        if not context.get("default_product_id"):
            raise UserError(_("No product found to generate Serials/Lots for."))
        assert mode in ("generate", "import")
        default_vals = {}

        def generate_lot_qty(quantity, qty_per_lot):
            if qty_per_lot <= 0:
                raise UserError(
                    _("The quantity per lot should always be a positive value.")
                )
            line_count = int(quantity // qty_per_lot)
            leftover = quantity % qty_per_lot
            qty_array = [qty_per_lot] * line_count
            if leftover:
                qty_array.append(leftover)
            return qty_array

        def remove_prefix(text, prefix):
            if text.startswith(prefix):
                return text[len(prefix) :]
            return text

        for key in context:
            if key.startswith("default_"):
                default_vals[remove_prefix(key, "default_")] = context[key]

        if default_vals["tracking"] == "lot" and mode == "generate":
            lot_qties = generate_lot_qty(default_vals["quantity"], count)
        else:
            lot_qties = [1] * count

        if mode == "generate":
            lot_names = self.env["stock.lot"].generate_lot_names(
                first_lot, len(lot_qties)
            )
        elif mode == "import":
            lot_names = self.split_lots(lot_text)
            lot_qties = [1] * len(lot_names)

        vals_list = []
        for lot, qty in zip(lot_names, lot_qties, strict=False):
            if not lot.get("quantity"):
                lot["quantity"] = qty
            loc_dest = self.env["stock.location"].browse(
                default_vals["location_dest_id"]
            )
            product = self.env["product.product"].browse(default_vals["product_id"])
            loc_dest = loc_dest._get_putaway_strategy(product, lot["quantity"])
            vals_list.append(
                {
                    **default_vals,
                    **lot,
                    "location_dest_id": loc_dest.id,
                    "product_uom_id": product.uom_id.id,
                }
            )

        if default_vals.get("picking_type_id"):
            picking_type = self.env["stock.picking.type"].browse(
                default_vals["picking_type_id"]
            )
            if mode == "import" and not picking_type.use_create_lots:
                self._search_lot_ids_from_move_line_vals(
                    vals_list, default_vals["product_id"], default_vals["company_id"]
                )
            elif picking_type.use_existing_lots:
                self._create_lot_ids_from_move_line_vals(
                    vals_list, default_vals["product_id"], default_vals["company_id"]
                )

        for values in vals_list:
            for key, value in values.items():
                if key in self.env["stock.move.line"] and isinstance(
                    self.env["stock.move.line"][key], models.Model
                ):
                    values[key] = {
                        "id": value,
                        "display_name": self.env["stock.move.line"][key]
                        .browse(value)
                        .display_name,
                    }
        return vals_list
