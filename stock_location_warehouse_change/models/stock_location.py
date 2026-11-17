# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import AccessError, UserError

WAREHOUSE_EDITOR_GROUP = "stock_location_warehouse_change.location_warehouse_editor"


class StockLocation(models.Model):
    _inherit = "stock.location"

    @api.depends("warehouse_view_ids", "location_id", "parent_path")
    def _compute_warehouse_id(self):
        new_locations = self.filtered(
            lambda location: isinstance(location.id, models.NewId)
        )
        for location in new_locations:
            location.warehouse_id = (
                location.warehouse_view_ids[:1] or location.location_id.warehouse_id
            )
        return super(StockLocation, self - new_locations)._compute_warehouse_id()

    def _can_change_warehouse(self):
        return self.env.su or self.env.user.has_group(WAREHOUSE_EDITOR_GROUP)

    def _check_warehouse_change(self, parent_location):
        if self._can_change_warehouse():
            return
        moved_locations = self.filtered(
            lambda location: (
                location.warehouse_view_ids[:1] or parent_location.warehouse_id
            )
            != location.warehouse_id
        )
        if moved_locations:
            raise UserError(
                _(
                    "You are not allowed to move these locations to another "
                    "warehouse: %(locations)s",
                    locations=", ".join(moved_locations.mapped("display_name")),
                )
            )

    def write(self, vals):
        if "location_id" in vals:
            self._check_warehouse_change(self.browse(vals["location_id"]))
        return super().write(vals)

    def action_recompute_warehouse(self):
        if not self._can_change_warehouse():
            raise AccessError(
                _("You are not allowed to recompute the warehouse of locations.")
            )
        locations = self.with_context(active_test=False).search(
            [("id", "child_of", self.ids)]
        )
        locations.modified(["parent_path"])
        locations.flush_recordset(["warehouse_id"])
