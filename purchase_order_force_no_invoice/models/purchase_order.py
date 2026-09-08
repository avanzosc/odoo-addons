# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    force_no_invoice = fields.Boolean(
        string="Force Nothing to Bill",
        help="If checked, the order's billing status is forced to "
        "'Nothing to Bill' even if there are lines or quantities "
        "still pending billing.",
    )

    @api.depends("force_no_invoice")
    def _get_invoiced(self):
        res = super()._get_invoiced()
        for order in self:
            if order.force_no_invoice:
                order.invoice_status = "no"
        return res
