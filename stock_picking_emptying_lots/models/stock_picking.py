# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    emptying_picking_id = fields.Many2one(comodel_name="stock.picking", copy=True)
    emptying_lots_type_id = fields.Many2one(
        comodel_name="stock.picking.type", domain="[('emptying_type', '=', True)]"
    )
    emptying_pickings_ids = fields.One2many(
        comodel_name="stock.picking",
        inverse_name="emptying_picking_id",
    )
    count_emptying_pickings = fields.Integer(compute="_compute_count_emptying_pickings")

    @api.depends("emptying_pickings_ids")
    def _compute_count_emptying_pickings(self):
        for picking in self:
            count = 0
            if picking.emptying_pickings_ids:
                count = len(picking.emptying_pickings_ids)
            picking.count_emptying_pickings = count

    def action_view_emptying_picking(self):
        context = self.env.context.copy()
        return {
            "name": _("Emptying Picking"),
            "view_mode": "tree,form",
            "res_model": "stock.picking",
            "domain": [("id", "in", self.emptying_pickings_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }

    def emptying_lots_in_location(self):
        for pick in self:
            if not pick.emptying_lots_type_id:
                raise exceptions.ValidationError(
                    _("You must introduce the emptying lots picking type.")
                )
            else:
                if pick.emptying_pickings_ids and any(
                    [
                        p.state not in ("done", "cancel")
                        for p in pick.emptying_pickings_ids
                    ]
                ):
                    picking = pick.emptying_pickings_ids.filtered(
                        lambda c: c.state not in ("done", "cancel")
                    )[:1]
                    for line in picking.move_line_ids_without_package:
                        line.unlink()
                    for move in picking.move_ids_without_package:
                        move.unlink()
                else:
                    picking = self.env["stock.picking"].create(
                        {
                            "emptying_picking_id": pick.id,
                            "picking_type_id": pick.emptying_lots_type_id.id,
                            "origin": pick.name,
                            "location_id": (
                                pick.emptying_lots_type_id.default_location_src_id.id
                            ),
                            "location_dest_id": (
                                pick.emptying_lots_type_id.default_location_dest_id.id
                            ),
                        }
                    )
                for line in pick.move_line_ids_without_package:
                    self.env["stock.move.line"].create_emptying_lots_movelines(
                        line=line, picking=picking
                    )
                picking.action_confirm()
