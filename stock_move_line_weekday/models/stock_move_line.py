# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    weekday = fields.Selection(
        selection=[
            ("1", "Monday"),
            ("2", "Tuesday"),
            ("3", "Wednesday"),
            ("4", "Thursday"),
            ("5", "Friday"),
            ("6", "Saturday"),
            ("7", "Sunday"),
        ],
        compute="_compute_date_fields",
        store=True,
    )
    year_week = fields.Integer(
        string="Week of Year",
        compute="_compute_date_fields",
        store=True,
    )
    month = fields.Selection(
        selection=[
            ("1", "January"),
            ("2", "February"),
            ("3", "March"),
            ("4", "April"),
            ("5", "May"),
            ("6", "June"),
            ("7", "July"),
            ("8", "August"),
            ("9", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ],
        compute="_compute_date_fields",
        store=True,
    )
    year = fields.Integer(
        compute="_compute_date_fields",
        store=True,
    )
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        compute="_compute_warehouse_id",
        store=True,
    )
    min_qty = fields.Float(
        string="Minimum Quantity",
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends("picking_id.picking_type_id.warehouse_id")
    def _compute_warehouse_id(self):
        for line in self:
            line.warehouse_id = line.picking_id.picking_type_id.warehouse_id

    @api.depends("picking_id.date_done", "date")
    def _compute_date_fields(self):
        for line in self:
            ref_dt = line.picking_id.date_done or line.date
            if ref_dt:
                d = ref_dt.date()
                line.weekday = str(d.isoweekday())
                line.year_week = d.isocalendar()[1]
                line.month = str(d.month)
                line.year = d.year
            else:
                line.weekday = False
                line.year_week = 0
                line.month = False
                line.year = 0

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._set_min_qty()
        return records

    def _action_done(self):
        res = super()._action_done()
        self._set_min_qty()
        return res

    def _set_min_qty(self):
        Orderpoint = self.env["stock.warehouse.orderpoint"]
        WeekdayRule = self.env["stock.warehouse.orderpoint.weekday"]

        valid_lines = self.filtered(lambda l: l.product_id and l.location_id)
        (self - valid_lines).write({"min_qty": 0.0})
        if not valid_lines:
            return

        all_ops = Orderpoint.search(
            [
                ("product_id", "in", valid_lines.product_id.ids),
                ("location_id", "in", valid_lines.location_id.ids),
            ]
        )
        ops_by_pl = {}
        for op in all_ops:
            ops_by_pl.setdefault((op.product_id.id, op.location_id.id), []).append(op)

        all_rules = (
            WeekdayRule.search(
                [
                    ("orderpoint_id", "in", all_ops.ids),
                    ("active", "=", True),
                ]
            )
            if all_ops
            else WeekdayRule.browse()
        )
        rules_by_op = {}
        for rule in all_rules:
            rules_by_op.setdefault(rule.orderpoint_id.id, []).append(rule)

        for line in valid_lines:
            ref_dt = line.picking_id.date_done or line.date
            ref_date = ref_dt.date() if ref_dt else None

            candidates = ops_by_pl.get((line.product_id.id, line.location_id.id), [])
            if line.warehouse_id:
                ops = [
                    op
                    for op in candidates
                    if op.warehouse_id.id == line.warehouse_id.id
                ]
            else:
                ops = candidates

            if not ops:
                line.min_qty = 0.0
                continue

            line_rules = [r for op in ops for r in rules_by_op.get(op.id, [])]
            min_qty = 0.0
            found = False

            if ref_date and line_rules:
                for rule in sorted(
                    (
                        r
                        for r in line_rules
                        if r.type_update == "specific" and r.specific_day == ref_date
                    ),
                    key=lambda r: r.sequence,
                ):
                    if rule.quantity:
                        min_qty = rule.quantity
                        found = True
                        break

                if not found:
                    weekday_str = str(ref_date.isoweekday())
                    for rule in sorted(
                        (
                            r
                            for r in line_rules
                            if r.type_update == "weekday" and r.weekday == weekday_str
                        ),
                        key=lambda r: r.sequence,
                    ):
                        if rule.quantity:
                            min_qty = rule.quantity
                            found = True
                            break

            if not found:
                min_qty = min(ops, key=lambda op: op.id).product_min_qty

            line.min_qty = min_qty
