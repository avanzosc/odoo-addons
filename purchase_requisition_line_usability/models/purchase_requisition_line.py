# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    vendor_id = fields.Many2one(
        string="Supplier",
        comodel_name="res.partner",
        related="requisition_id.vendor_id",
        store=True)
    user_id = fields.Many2one(
        string="Supplier's Representative",
        comodel_name="res.users",
        related="requisition_id.user_id",
        store=True)
    type_id = fields.Many2one(
        string="Purchase Requisition Type",
        comodel_name="purchase.requisition.type",
        related="requisition_id.type_id",
        store=True)
    price_unit = fields.Float(
        digits="Price Unit Decimal Precision")
    shipping_cost = fields.Float(
        string="Shipping Cost",
        digits="Price Unit Decimal Precision")
    date_end = fields.Datetime(
        string="Date End",
        related="requisition_id.date_end",
        store=True)
    ordering_date = fields.Date(
        string="Ordering Date",
        related="requisition_id.ordering_date",
        store=True)
    schedule_date = fields.Date(
        string="Schedule Date",
        related="requisition_id.schedule_date",
        store=True)
    state = fields.Selection(
        string="State",
        related="requisition_id.state",
        store=True)
    origin = fields.Char(
        string="Origin Document",
        related="requisition_id.origin",
        store=True)
    dif_qty = fields.Float(
        string="Pending",
        compute="_compute_dif_qty")

    @api.depends("product_qty", "qty_ordered")
    def _compute_dif_qty(self):
        for line in self:
            line.dif_qty = line.product_qty - line.qty_ordered
