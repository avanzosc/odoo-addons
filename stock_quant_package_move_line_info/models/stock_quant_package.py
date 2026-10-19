# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    move_lines_ids = fields.One2many(
        string="Move Lines", comodel_name="stock.move.line", inverse_name="package_id"
    )
    result_move_lines_ids = fields.One2many(
        string="result Move Lines",
        comodel_name="stock.move.line",
        inverse_name="result_package_id",
    )
    move_lines_count = fields.Integer(
        string="Num. Move Lines", compute="_compute_move_lines_count", store=True
    )
    without_performing_move_lines_count = fields.Integer(
        string="Without Performing Num. Move Lines",
        compute="_compute_without_performing_move_lines_count",
        store=True,
    )
    all_quant_ids = fields.One2many(
        string="All Quants", comodel_name="stock.quant", inverse_name="package_id"
    )

    @api.depends("move_lines_ids", "result_move_lines_ids")
    def _compute_move_lines_count(self):
        for package in self:
            lines = package.move_lines_ids | package.result_move_lines_ids
            package.move_lines_count = len(lines)

    @api.depends(
        "move_lines_ids",
        "move_lines_ids.state",
        "result_move_lines_ids",
        "result_move_lines_ids.state",
    )
    def _compute_without_performing_move_lines_count(self):
        for package in self:
            move_lines = package.move_lines_ids.filtered(
                lambda x: x.state not in ("done", "cancel")
            )
            result_move_lines = package.result_move_lines_ids.filtered(
                lambda x: x.state not in ("done", "cancel")
            )
            lines = move_lines | result_move_lines
            package.without_performing_move_lines_count = len(lines)

    def action_view_move_lines_from_package(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.stock_move_line_action"
        )
        lines = self.move_lines_ids | self.result_move_lines_ids
        action["domain"] = [("id", "in", lines.ids)]
        return action
