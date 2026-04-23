# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    sale_order_line_history_count = fields.Integer(
        string="Sales History Lines",
        compute="_compute_sale_order_line_history_count",
    )

    def _compute_sale_order_line_history_count(self):
        commercial_partners = self.mapped("commercial_partner_id")
        counts = {}
        if commercial_partners:
            grouped = (
                self.env["sale.order.line.history.report"]
                .sudo()
                .read_group(
                    domain=[("commercial_partner_id", "in", commercial_partners.ids)],
                    fields=["commercial_partner_id"],
                    groupby=["commercial_partner_id"],
                )
            )
            counts = {
                group["commercial_partner_id"][0]: group["commercial_partner_id_count"]
                for group in grouped
                if group.get("commercial_partner_id")
            }
        for partner in self:
            partner.sale_order_line_history_count = counts.get(
                partner.commercial_partner_id.id, 0
            )

    def action_open_sale_order_line_history(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_import_wizard_history.sale_order_line_history_report_action"
        )
        action["domain"] = [
            ("commercial_partner_id", "=", self.commercial_partner_id.id),
        ]
        action["context"] = {"search_default_group_partner": 1}
        return action
