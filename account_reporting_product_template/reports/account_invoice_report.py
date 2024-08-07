# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
    )

    @api.model
    def _select(self):
        select_str = super()._select()
        select_str += """
            , template.id as product_tmpl_id
            """
        return select_str

    @api.model
    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += ", template.id"
        return group_by_str
