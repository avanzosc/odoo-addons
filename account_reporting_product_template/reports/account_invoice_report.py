# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
    )

    @api.model
    def _select(self):
        return SQL(
            """
            %s,
            product.product_tmpl_id AS product_tmpl_id
        """,
            super()._select(),
        )
