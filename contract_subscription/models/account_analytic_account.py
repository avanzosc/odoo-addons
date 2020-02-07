# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    invoice_project_id = fields.Many2one(
        comodel_name="project.project", string="Related Project")

    @api.model
    def _prepare_invoice_line(self, line, invoice_id):
        invoice_line_vals = super(AccountAnalyticAccount,
                                  self)._prepare_invoice_line(line, invoice_id)
        contract_project = line.analytic_account_id.invoice_project_id
        if contract_project:
            invoice_line_vals.update({
                "account_analytic_id": contract_project.analytic_account_id.id,
            })
        return invoice_line_vals
