# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    @api.depends("quant_package_ids")
    def _compute_packages_qty(self):
        for picking in self:
            picking.packages_qty = len(picking.quant_package_ids)

    quant_package_ids = fields.One2many(
        string="Packages", comodel_name="stock.quant.package", inverse_name="batch_id"
    )
    qty_packages = fields.Integer(string="Number of Packages")
    packages_qty = fields.Integer(
        string="Packages Quantity", compute="_compute_packages_qty", store=True
    )

    def action_view_package(self):
        context = self.env.context.copy()
        context.update({"default_batch_id": self.id})
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
        pack_vals = {"batch_id": self.id}
        for i in range(1, self.qty_packages + 1):
            name = "{} {} {:0>3}".format(self.name, "-", i)
            pack_vals.update({"name": name})
            self.env["stock.quant.package"].create(pack_vals)
