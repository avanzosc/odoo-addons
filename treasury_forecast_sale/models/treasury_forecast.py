# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


class TreasuryForecast(models.Model):
    _inherit = "treasury.forecast"

    sale_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Sale Order Line",
        copy=False,
        readonly=True,
        index=True,
    )

    def _get_sale_order_project(self):
        if any(not line.project_id for line in self):
            raise UserError(_("All selected treasury lines must have a project."))
        projects = self.project_id
        if len(projects) != 1:
            raise UserError(
                _("All selected treasury lines must belong to one project.")
            )
        return projects

    def action_create_sale_order(self, partner):
        project = self._get_sale_order_project()
        if not partner:
            raise UserError(
                _(
                    "A sales quotation cannot be created because no customer has "
                    "been assigned."
                )
            )
        forecast_lines = self.filtered(lambda line: line.income > 0)
        project.partner_id = partner
        order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "project_id": project.id,
            }
        )
        for forecast_line in forecast_lines:
            sale_line = self.env["sale.order.line"].create(
                {
                    "order_id": order.id,
                    "product_id": forecast_line.product_id.id,
                    "product_uom_qty": forecast_line.quantity,
                    "price_unit": forecast_line.income_price,
                }
            )
            forecast_line.sale_line_id = sale_line

        return {
            "type": "ir.actions.act_window",
            "name": _("Sales Quotation"),
            "res_model": "sale.order",
            "res_id": order.id,
            "view_mode": "form",
            "target": "current",
        }
