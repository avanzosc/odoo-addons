# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    segment_id = fields.Many2one(
        comodel_name="partner.segment",
        string="Segment",
        readonly=True,
    )

    @api.model
    def _select(self):
        return SQL("%s, partner.segment_id as segment_id", super()._select())
