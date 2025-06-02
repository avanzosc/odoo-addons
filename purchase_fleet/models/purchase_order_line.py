# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    purchase_vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Purchase for Vehicle",
        compute="_compute_purchase_vehicle",
        inverse="_inverse_purchase_vehicle",
        store=True,
    )

    @api.depends("account_analytic_id", "product_id", "date_order")
    def _compute_purchase_vehicle(self):
        for line in self:
            line.purchase_vehicle_id = line.account_analytic_id.vehicle_id

    def _inverse_purchase_vehicle(self):
        for line in self:
            if line.account_analytic_id:
                line.account_analytic_id.vehicle_id = line.purchase_vehicle_id
