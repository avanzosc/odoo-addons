# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

PURCHASE_REQUISITION_STATES = [
    ("draft", "Draft"),
    ("ongoing", "Ongoing"),
    ("in_progress", "Confirmed"),
    ("open", "Bid Selection"),
    ("done", "Closed"),
    ("cancel", "Cancelled"),
]


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    user_id = fields.Many2one(
        string="Purchase Representative",
        comodel_name="res.users",
        related="requisition_id.user_id",
        store=True,
        copy=False,
    )
    vendor_id = fields.Many2one(
        string="Vendor",
        comodel_name="res.partner",
        related="requisition_id.vendor_id",
        store=True,
        copy=False,
    )
    ordering_date = fields.Date(
        string="Ordering Date",
        related="requisition_id.ordering_date",
        store=True,
        copy=False,
    )
    date_end = fields.Datetime(
        string="Agreement Deadline",
        related="requisition_id.date_end",
        store=True,
        copy=False,
    )
    schedule_date = fields.Date(
        string="Delivery Date",
        related="requisition_id.schedule_date",
        store=True,
        copy=False,
    )
    state = fields.Selection(
        PURCHASE_REQUISITION_STATES,
        string="Status",
        related="requisition_id.state",
        store=True,
        copy=False,
    )
