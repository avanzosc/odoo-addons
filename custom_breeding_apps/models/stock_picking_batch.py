# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        result = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        if not name:
            return result
        my_name = "%{}%".format(name)
        cond = [
            "|",
            ("location_id", operator, my_name),
            ("warehouse_id", operator, my_name),
        ]
        batches = self.sudo().search(cond)
        for batch in batches:
            found = False
            for line in result:
                if line and line[0] == batch.id:
                    found = True
                    break
            if not found:
                result.append((batch.id, batch.name))
        return result

    def _compute_eggs_count(self):
        for batch in self:
            batch.egg_count = len(batch.egg_ids)

    egg_ids = fields.One2many(
        string="Eggs", comodel_name="stock.move.line", inverse_name="batch_id"
    )
    egg_count = fields.Integer("# Eggs", compute="_compute_eggs_count")
    quant_ids = fields.One2many(
        string="Stock", comodel_name="stock.quant", compute="_compute_quant_ids"
    )
    chick_entry_qty = fields.Integer(
        string="Chick Entry Qty", compute="_compute_chick_entry_qty"
    )
    chick_outflow_qty = fields.Integer(
        string="Chick Outflow Qty", compute="_compute_chick_outflow_qty"
    )
    chick_existence = fields.Float(
        string="Chick Existence", compute="_compute_chick_existece"
    )

    def _compute_chick_entry_qty(self):
        for batch in self:
            chick_entry_qty = 0
            if batch.move_line_ids and batch.batch_type == "breeding":
                chick_entry_qty = sum(
                    batch.move_line_ids.filtered(
                        lambda c: c.product_id.one_day_chicken is True
                        and (c.state == "done")
                        and c.location_dest_id == (batch.location_id)
                    ).mapped("qty_done")
                )
            batch.chick_entry_qty = chick_entry_qty

    def _compute_chick_outflow_qty(self):
        for batch in self:
            chick_outflow_qty = 0
            if batch.move_line_ids and batch.batch_type == "breeding":
                chick_outflow_qty = sum(
                    batch.move_line_ids.filtered(
                        lambda c: c.product_id.one_day_chicken is True
                        and (c.state == "done")
                        and c.location_id == (batch.location_id)
                    ).mapped("qty_done")
                ) + sum(
                    batch.move_line_ids.filtered(
                        lambda c: c.saca_line_id and (c.state == "done")
                    ).mapped("qty_done")
                )
            batch.chick_outflow_qty = chick_outflow_qty

    def _compute_chick_existece(self):
        for batch in self:
            batch.chick_existence = batch.chick_entry_qty - batch.chick_outflow_qty

    def _compute_quant_ids(self):
        for batch in self:
            quant_ids = False
            if batch.location_id:
                cond = [("location_id", "=", batch.location_id.id)]
                if batch.location_id.child_ids:
                    cond = [("location_id", "in", (batch.location_id.child_ids.ids))]
                quant = self.env["stock.quant"].search(cond)
                quant_ids = [(6, 0, quant.ids)]
            batch.quant_ids = quant_ids

    def action_view_eggs(self):
        context = self.env.context.copy()
        context.update({"default_batch_id": self.id})
        domain = [("id", "in", self.egg_ids.ids), ("qty_done", "!=", 0)]
        return {
            "name": _("Eggs"),
            "view_mode": "tree",
            "res_model": "stock.move.line",
            "domain": domain,
            "type": "ir.actions.act_window",
            "context": context,
        }

    def action_view_quant_ids(self):
        context = self.env.context.copy()
        context.update({"default_picking_id": self.id})
        if self.location_id.child_ids:
            context.update({"search_default_locationgroup": 1})
        else:
            context.update({"search_default_productgroup": 1})
        return {
            "name": _("Stock"),
            "view_mode": "tree",
            "res_model": "stock.quant",
            "domain": [("id", "in", self.quant_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }
