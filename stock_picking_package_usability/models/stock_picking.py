# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends("quant_package_ids", "quant_package_ids.shipping_weight")
    def _compute_packages_weight(self):
        for picking in self:
            picking.packages_weight = sum(
                picking.quant_package_ids.mapped("shipping_weight")
            )

    @api.depends("quant_package_ids", "quant_package_ids.volume")
    def _compute_packages_volume(self):
        for picking in self:
            picking.packages_volume = sum(picking.quant_package_ids.mapped("volume"))

    @api.depends("quant_package_ids")
    def _compute_packages_qty(self):
        for picking in self:
            picking.packages_qty = len(picking.quant_package_ids)

    def _compute_volume_uom_name(self):
        for package in self:
            if package.quant_package_ids:
                package.volume_uom_name = package.quant_package_ids[0].volume_uom_name

    @api.depends("packages_qty", "packages_weight", "weight_uom_name")
    def _compute_packages_qty_weight(self):
        for picking in self:
            picking.packages_qty_weight = "{} {} {} {}".format(
                picking.packages_qty,
                "-",
                picking.packages_weight,
                picking.weight_uom_name,
            )

    quant_package_ids = fields.One2many(
        string="Packages", comodel_name="stock.quant.package", inverse_name="picking_id"
    )
    packages_qty_weight = fields.Char(
        string="# Packages", compute="_compute_packages_qty_weight", store=True
    )
    qty_packages = fields.Integer(string="Number of Packages")
    packages_weight = fields.Float(
        string="Packages Weight", compute="_compute_packages_weight", store=True
    )
    packages_volume = fields.Float(
        string="Packages Volume", compute="_compute_packages_volume", store=True
    )
    volume_uom_name = fields.Char(
        string="Volume UOM", compute="_compute_volume_uom_name", store=True
    )
    packages_qty = fields.Integer(
        string="Packages Quantity", compute="_compute_packages_qty", store=True
    )

    def action_view_package(self):
        context = self.env.context.copy()
        context.update({"default_picking_id": self.id})
        return {
            "name": _("Packages"),
            "view_mode": "tree",
            "res_model": "stock.quant.package",
            "domain": [("id", "in", self.quant_package_ids.ids)],
            "type": "ir.actions.act_window",
            "view_id": self.env.ref(
                "stock_picking_package_usability.stock_quant_package_view_tree"
            ).id,
            "context": context,
        }

    def action_create_package(self):
        self.ensure_one()
        pack_vals = {"picking_id": self.id}
        for i in range(1, self.qty_packages + 1):
            name = "{} {} {:0>3}".format(self.name, "-", i)
            pack_vals.update({"name": name})
            self.env["stock.quant.package"].create(pack_vals)

    def _put_in_pack(self, move_line_ids, create_package_level=True):
        move_line_ids = move_line_ids.filtered(lambda x: not x.result_package_id)
        if move_line_ids:
            result = super()._put_in_pack(move_line_ids, create_package_level=True)
            result.name = "{} {} {:0>3}".format(
                self.name, "-", len(self.quant_package_ids)
            )
            return result
