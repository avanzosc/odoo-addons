# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.depends(
        "supplier_id",
        "product_id",
        "product_id.orderpoint_ids",
        "product_id.orderpoint_ids.supplier_id",
        "product_id.orderpoint_ids.supplier_id.certification_id",
    )
    def _compute_certification_id(self):
        for orderpoint in self:
            certification_id = self.env["product.supplierinfo.certification"]
            if orderpoint.product_id and orderpoint.supplier_id:
                lines = orderpoint.product_id.orderpoint_ids.filtered(
                    lambda x: x.supplier_id.id == orderpoint.supplier_id.id
                )
                line = False
                if lines and len(lines) == 1:
                    line = lines
                if lines and len(lines) > 1:
                    line = min(lines, key=lambda x: x.sequence)
                if line and line.supplier_id.certification_id:
                    certification_id = line.supplier_id.certification_id.id
            orderpoint.certification_id = certification_id

    certification_id = fields.Many2one(
        string="Supplier qualification",
        comodel_name="product.supplierinfo.certification",
        compute="_compute_certification_id",
        copy=False,
        store=True,
    )
