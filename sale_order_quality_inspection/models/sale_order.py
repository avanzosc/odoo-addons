# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    quality_inspection_count = fields.Integer(
        string="Quality Inspections",
        compute="_compute_quality_inspection_count",
    )

    def _compute_quality_inspection_count(self):
        inspection_obj = self.env["qc.inspection"]
        for order in self:
            domain = [
                "|",
                ("production_id.sale_id", "=", order.id),
                ("picking_id", "in", order.picking_ids.ids),
            ]
            order.quality_inspection_count = inspection_obj.search_count(domain)

    def action_view_quality_inspections(self):
        self.ensure_one()
        domain = [
            "|",
            ("production_id.sale_id", "=", self.id),
            ("picking_id", "in", self.picking_ids.ids),
        ]
        inspections = self.env["qc.inspection"].search(domain)
        result = self.env["ir.actions.actions"]._for_xml_id(
            "quality_control_oca.action_qc_inspection"
        )
        result["context"] = {}
        result["domain"] = [("id", "in", inspections.ids)]
        return result
