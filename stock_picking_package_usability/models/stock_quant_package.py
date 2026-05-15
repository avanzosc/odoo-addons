# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    picking_id = fields.Many2one(string="Transfer", comodel_name="stock.picking")
    max_weight = fields.Float(
        string="Maximum Weight", related="product_packaging_id.max_weight", store=True
    )
    pack_length = fields.Float()
    width = fields.Float(string="Pack Width")
    height = fields.Float(string="Pack Height")
    partner_id = fields.Many2one(
        string="Delivery Address",
        comodel_name="res.partner",
        related="picking_id.partner_id",
        store=True,
    )
    move_line_ids = fields.One2many(
        comodel_name="stock.move.line",
        inverse_name="result_package_id",
        string="Move Lines",
    )
    shipping_weight = fields.Float(
        compute="_compute_shipping_weight",
        store=True,
        readonly=False,
    )

    @api.depends(
        "product_packaging_id.weight",
        "picking_id",
        "move_line_ids.line_weight",
        "move_line_ids.picking_id",
    )
    def _compute_shipping_weight(self):
        for pkg in self:
            empty = pkg.product_packaging_id.weight if pkg.product_packaging_id else 0.0
            lines = pkg.move_line_ids
            if pkg.picking_id:
                lines = lines.filtered(
                    lambda line, p=pkg: line.picking_id == p.picking_id
                )
            pkg.shipping_weight = empty + sum(lines.mapped("line_weight"))

    def write(self, vals):
        res = super().write(vals)
        if "product_packaging_id" in vals:
            move_lines = self.env["stock.move.line"].search(
                [("result_package_id", "in", self.ids)]
            )
            for package in self:
                lines = move_lines.filtered(
                    lambda line, pkg=package: line.result_package_id == pkg
                )
                if lines:
                    lines.with_context(
                        skip_package_sync=True
                    ).packaging_id = package.product_packaging_id
        return res

    def action_open_package(self):
        self.ensure_one()
        return {
            "name": "Package",
            "type": "ir.actions.act_window",
            "res_model": "stock.quant.package",
            "res_id": self.id,
            "view_mode": "form",
            "views": [(self.env.ref("stock.view_quant_package_form").id, "form")],
            "target": "current",
        }
