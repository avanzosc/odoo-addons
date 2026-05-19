# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        result = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        if not name:
            return result
        my_name = f"%{name}%"
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
    egg_count = fields.Integer(
        string="# Eggs",
        compute="_compute_eggs_count",
    )
    quant_ids = fields.One2many(
        string="Stock", comodel_name="stock.quant", compute="_compute_quant_ids"
    )
    chick_entry_qty = fields.Integer(compute="_compute_chick_entry_qty")
    chick_outflow_qty = fields.Integer(compute="_compute_chick_outflow_qty")
    chick_existence = fields.Float(compute="_compute_chick_existece")
    rvd_number = fields.Char(
        string="RVD No.",
        help="Responsible Veterinary Declaration (RVD) Number",
        default=lambda self: self.env.company.rvd_number,
    )

    @api.onchange("company_id")
    def _onchange_company_rvd(self):
        for record in self:
            record.rvd_number = record.company_id.rvd_number

    @api.constrains("rvd_number")
    def _check_rvd_number(self):
        for record in self.filtered("rvd_number"):
            if len(record.rvd_number) != 12 or not record.rvd_number.isdigit():
                raise ValidationError(
                    _("The RVD number must contain exactly 12 numeric digits.")
                )

    def _compute_chick_entry_qty(self):
        for batch in self:
            chick_entry_qty = 0
            if batch.move_line_ids and batch.batch_type == "breeding":
                chick_entry_qty = sum(
                    batch.move_line_ids.filtered(
                        lambda c, _batch=batch: c.product_id.one_day_chicken is True
                        and (c.state == "done")
                        and c.location_dest_id == (_batch.location_id)
                    ).mapped("quantity")
                )
            batch.chick_entry_qty = chick_entry_qty

    def _compute_chick_outflow_qty(self):
        for batch in self:
            chick_outflow_qty = 0
            if batch.move_line_ids and batch.batch_type == "breeding":
                chick_outflow_qty = sum(
                    batch.move_line_ids.filtered(
                        lambda c, _batch=batch: c.product_id.one_day_chicken is True
                        and (c.state == "done")
                        and c.location_id == (_batch.location_id)
                    ).mapped("quantity")
                ) + sum(
                    batch.move_line_ids.filtered(
                        lambda c: c.saca_line_id and (c.state == "done")
                    ).mapped("quantity")
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
        domain = [("id", "in", self.egg_ids.ids), ("quantity", "!=", 0)]
        return {
            "name": _("Eggs"),
            "view_mode": "list",
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
            "view_mode": "list",
            "res_model": "stock.quant",
            "domain": [("id", "in", self.quant_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }
