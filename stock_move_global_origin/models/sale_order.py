# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from psycopg2 import sql

from odoo import api, fields, models

_MODELS_WITH_GLOBAL_ORIGIN = (
    ("sale.order", "sale_order"),
    ("purchase.order", "purchase_order"),
    ("mrp.production", "mrp_production"),
    ("stock.move", "stock_move"),
    ("stock.move.line", "stock_move_line"),
)
_TABLE_BY_MODEL = dict(_MODELS_WITH_GLOBAL_ORIGIN)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    global_origin_initial = fields.Boolean(string="Initial", copy=False)
    global_origin = fields.Char(compute="_compute_global_origin", store=True)

    @api.depends(
        "name", "global_origin_initial", "auto_purchase_order_id.global_origin"
    )
    def _compute_global_origin(self):
        for order in self:
            order.global_origin = order.auto_purchase_order_id.global_origin or (
                order.name if order.global_origin_initial else False
            )

    def write(self, vals):
        to_propagate = self.env["sale.order"]
        cleared_origins = []
        if "global_origin_initial" in vals:
            if vals["global_origin_initial"]:
                to_propagate = self.filtered(lambda o: not o.global_origin_initial)
            else:
                cleared_origins = self.filtered("global_origin_initial").mapped(
                    "global_origin"
                )
        res = super().write(vals)
        if cleared_origins:
            self._clear_global_origin(cleared_origins)
        if to_propagate:
            to_propagate._propagate_global_origin()
        return res

    def _propagate_global_origin(self):
        for order in self:
            origin = order.global_origin
            if not origin:
                continue
            seen_moves = self.env["stock.move"]
            frontier = self.env["stock.move"].search(
                [("sale_line_id", "in", order.order_line.ids)]
            )
            while frontier:
                seen_moves |= frontier
                frontier = (
                    frontier.move_orig_ids | frontier.move_dest_ids
                ) - seen_moves

            purchase_orders = seen_moves.purchase_line_id.order_id
            productions = (
                seen_moves.raw_material_production_id | seen_moves.production_id
            )
            sale_orders = seen_moves.sale_line_id.order_id | order

            self._write_global_origin(seen_moves, origin)
            self._write_global_origin(seen_moves.move_line_ids, origin)
            self._write_global_origin(purchase_orders, origin)
            self._write_global_origin(productions, origin)
            self._write_global_origin(sale_orders, origin)

    def _clear_global_origin(self, origins):
        origins = [origin for origin in origins if origin]
        if not origins:
            return
        for model_name, table in _MODELS_WITH_GLOBAL_ORIGIN:
            self.env.cr.execute(
                sql.SQL(
                    "UPDATE {} SET global_origin = NULL"
                    " WHERE global_origin = ANY(%s)"
                ).format(sql.Identifier(table)),
                (origins,),
            )
            self.env[model_name].invalidate_cache(fnames=["global_origin"])

    def _write_global_origin(self, records, value):
        if not records:
            return
        self.env.cr.execute(
            sql.SQL("UPDATE {} SET global_origin = %s WHERE id = ANY(%s)").format(
                sql.Identifier(_TABLE_BY_MODEL[records._name])
            ),
            (value, records.ids),
        )
        self.env[records._name].invalidate_cache(fnames=["global_origin"])
