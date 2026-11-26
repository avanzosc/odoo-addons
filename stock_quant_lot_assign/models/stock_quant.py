# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import AccessError, UserError
from odoo.tools import float_compare, float_is_zero, float_round

LOT_PREFIX_PARAM = "stock_quant_lot_assign.lot_prefix"
DEFAULT_LOT_PREFIX = "BORRAR"
LOT_SEQUENCE_CODE = "stock.quant.lot.assign"


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _get_quants_to_assign_lot(self):
        """Quants of products tracked by lots or serial numbers, without lot
        and with positive quantity in internal or transit locations."""
        return self.filtered(
            lambda quant: quant.product_id.tracking in ("lot", "serial")
            and not quant.lot_id
            and quant.location_id.usage in ("internal", "transit")
            and float_compare(
                quant.quantity, 0, precision_rounding=quant.product_uom_id.rounding
            )
            > 0
        )

    def _check_assign_lot_serial_quantities(self):
        """Quants of products tracked by serial numbers must have a whole
        quantity, as one serial number is created per unit."""
        wrong_quants = self.filtered(
            lambda quant: quant.product_id.tracking == "serial"
            and not float_is_zero(
                quant.quantity - float_round(quant.quantity, precision_digits=0),
                precision_rounding=quant.product_uom_id.rounding,
            )
        )
        if wrong_quants:
            raise UserError(
                _(
                    "The following quants of products tracked by serial numbers "
                    "do not have a whole quantity, so one serial number per unit "
                    "cannot be created:\n%(quants)s",
                    quants=wrong_quants._get_assign_lot_quants_description(),
                )
            )

    def _get_assign_lot_quants_description(self):
        return "\n".join(
            f"- {quant.product_id.display_name} ({quant.location_id.display_name}): "
            f"{quant.quantity} {quant.product_uom_id.name}"
            for quant in self
        )

    def _get_assign_lot_reserved_moves(self):
        """Moves with quantities reserved in the quants."""
        move_lines = self.env["stock.move.line"]
        for quant in self:
            move_lines |= self.env["stock.move.line"].search(
                [
                    ("product_id", "=", quant.product_id.id),
                    ("location_id", "=", quant.location_id.id),
                    ("lot_id", "=", False),
                    ("package_id", "=", quant.package_id.id),
                    ("owner_id", "=", quant.owner_id.id),
                    ("state", "not in", ("done", "cancel")),
                    ("move_id", "!=", False),
                ]
            )
        return move_lines.move_id

    def _unreserve_assign_lot_quants(self):
        """Unreserve the quantities reserved in the quants, and return the
        unreserved moves so they can be reserved again afterwards."""
        reserved_quants = self.filtered(
            lambda quant: float_compare(
                quant.reserved_quantity,
                0,
                precision_rounding=quant.product_uom_id.rounding,
            )
            > 0
        )
        if not reserved_quants:
            return self.env["stock.move"]
        moves = reserved_quants._get_assign_lot_reserved_moves()
        moves._do_unreserve()
        still_reserved = reserved_quants.filtered(
            lambda quant: float_compare(
                quant.reserved_quantity,
                0,
                precision_rounding=quant.product_uom_id.rounding,
            )
            > 0
        )
        if still_reserved:
            raise UserError(
                _(
                    "The reservations of the following quants cannot be undone, "
                    "probably because their operations are already picked. "
                    "Unpick or process those operations first:\n%(quants)s",
                    quants=still_reserved._get_assign_lot_quants_description(),
                )
            )
        return moves

    def _get_assign_lot_prefix(self):
        prefix = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(LOT_PREFIX_PARAM, DEFAULT_LOT_PREFIX)
        )
        return prefix or DEFAULT_LOT_PREFIX

    def _get_assign_lot_name(self, prefix):
        """Return a lot name not used yet for the product and company of the
        quant."""
        self.ensure_one()
        sequence_obj = self.env["ir.sequence"].sudo()
        lot_obj = self.env["stock.lot"].sudo().with_context(active_test=False)
        while True:
            name = f"{prefix}{sequence_obj.next_by_code(LOT_SEQUENCE_CODE)}"
            if not lot_obj.search_count(
                [
                    ("name", "=", name),
                    ("product_id", "=", self.product_id.id),
                    ("company_id", "in", [self.company_id.id, False]),
                ]
            ):
                return name

    def _prepare_assign_lot_vals(self, prefix):
        self.ensure_one()
        return {
            "name": self._get_assign_lot_name(prefix),
            "product_id": self.product_id.id,
            "company_id": self.company_id.id,
        }

    def _prepare_assign_lot_quant_vals(self, lot, quantity):
        self.ensure_one()
        return {
            "product_id": self.product_id.id,
            "location_id": self.location_id.id,
            "lot_id": lot.id,
            "package_id": self.package_id.id,
            "owner_id": self.owner_id.id,
            "inventory_quantity": quantity,
        }

    def _get_assign_lot_quantities(self):
        """Quantities of the new quants: the whole quantity for products
        tracked by lots, and one unit per serial number for products tracked by
        serial numbers."""
        self.ensure_one()
        if self.product_id.tracking == "serial":
            return [1.0] * int(float_round(self.quantity, precision_digits=0))
        return [self.quantity]

    def action_assign_lot(self):
        """Assign new lots or serial numbers to the selected quants without
        lot.

        The quant is not modified directly. For each quant, an inventory
        adjustment moves its quantity out of the quant without lot and into
        new quants with the new lots: one quant with the whole quantity for
        products tracked by lots, and one quant per unit for products tracked
        by serial numbers. Stock moves, traceability and valuation stay
        consistent.

        Quantities reserved in the quants are unreserved first, and the
        unreserved moves are reserved again at the end.
        """
        if not self.env.user.has_group("stock.group_stock_manager"):
            raise AccessError(
                _("Only inventory administrators can assign lots to quants.")
            )
        quants = self._get_quants_to_assign_lot()
        if not quants:
            raise UserError(
                _(
                    "None of the selected quants can be processed. Only quants "
                    "without lot, with positive quantity in internal or transit "
                    "locations, of products tracked by lots or serial numbers "
                    "are processed."
                )
            )
        quants._check_assign_lot_serial_quantities()
        unreserved_moves = quants._unreserve_assign_lot_quants()
        prefix = self._get_assign_lot_prefix()
        quant_obj = self.env["stock.quant"].with_context(inventory_mode=True)
        lot_obj = self.env["stock.lot"]
        new_quants = self.env["stock.quant"]
        for quant in quants:
            for quantity in quant._get_assign_lot_quantities():
                lot = lot_obj.create(quant._prepare_assign_lot_vals(prefix))
                new_quants |= quant_obj.create(
                    quant._prepare_assign_lot_quant_vals(lot, quantity)
                )
            quant.with_context(inventory_mode=True).write(
                {"inventory_quantity": 0.0, "inventory_quantity_set": True}
            )
        (quants | new_quants).with_context(
            inventory_name=_("Lot assignment")
        )._apply_inventory()
        if unreserved_moves:
            unreserved_moves.filtered(
                lambda move: move.state not in ("done", "cancel")
            )._action_assign()
        action = self.env["stock.quant"].action_view_inventory()
        action["domain"] = [("id", "in", new_quants.ids)]
        return action
