# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    picking_id = fields.Many2one(string="Transfer", comodel_name="stock.picking")
    max_weight = fields.Float(
        string="Maximum Weight", related="packaging_id.max_weight", store=True
    )
    pack_length = fields.Float(string="Pack Length")
    width = fields.Float(string="Pack Width")
    height = fields.Float(string="Pack Height")
    partner_id = fields.Many2one(
        string="Delivery Address",
        comodel_name="res.partner",
        related="picking_id.partner_id",
        store=True,
    )

    move_line_ids = fields.One2many(
        "stock.move.line",
        "result_package_id",
        string="Move Lines",
    )

    shipping_weight = fields.Float(
        compute="_compute_shipping_weight", store=True, readonly=False
    )

    @api.depends(
        "packaging_id.empty_weight",
        "picking_id",
        "move_line_ids.line_weight",
        "move_line_ids.picking_id",
    )
    def _compute_shipping_weight(self):
        for pkg in self:
            empty = (pkg.packaging_id.empty_weight or 0.0) if pkg.packaging_id else 0.0
            lines = pkg.move_line_ids
            if pkg.picking_id:
                lines = lines.filtered(lambda l: l.picking_id.id == pkg.picking_id.id)
            pkg.shipping_weight = empty + sum(lines.mapped("line_weight"))

    @api.depends("shipping_weight")
    def _compute_estimated_pack_weight_kg(self):
        for pkg in self:
            pkg.estimated_pack_weight_kg = pkg.shipping_weight

    @api.onchange("packaging_id")
    def onchange_dimension(self):
        if self.packaging_id.height:
            self.height = self.packaging_id.height
        if self.packaging_id.width:
            self.width = self.packaging_id.width
        if self.packaging_id.packaging_length:
            self.pack_length = self.packaging_id.packaging_length
        if self.packaging_id.length_uom_id:
            self.length_uom_id = self.packaging_id.length_uom_id.id
        if self.packaging_id.volume_uom_id:
            self.volume_uom_id = self.packaging_id.volume_uom_id.id
        if self.packaging_id.weight_uom_id:
            self.weight_uom_id = self.packaging_id.weight_uom_id.id
        if self.packaging_id.volume:
            self.volume = self.packaging_id.volume

    @api.model
    def create(self, vals):
        line = super().create(vals)
        line.name = "{} {} {:0>3}".format(
            line.picking_id.name, "-", len(line.picking_id.quant_package_ids)
        )
        return line

    def action_open_package(self):
        self.ensure_one()
        return {
            "name": "Paquete",
            "type": "ir.actions.act_window",
            "res_model": "stock.quant.package",
            "res_id": self.id,
            "view_mode": "form",
            "views": [(self.env.ref("stock.view_quant_package_form").id, "form")],
            "target": "current",
        }
