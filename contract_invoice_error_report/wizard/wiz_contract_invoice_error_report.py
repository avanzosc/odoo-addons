# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.osv import expression


class WizContractInvoiceErrorReport(models.TransientModel):
    _name = "wiz.contract.invoice.error.report"
    _description = "Wizard for find errors in invoice generation from contrats"

    def process(self):
        self.ensure_one()
        contract_obj = self.env["contract.contract"]
        contracts = contract_obj.sudo().search([])
        contracts.write(
            {"with_invoice_generation_error": False, "invoice_generation_error": ""}
        )
        self.sudo()._cron_recurring_create(date_ref=fields.Date.context_today(self))

    @api.model
    def _cron_recurring_create(self, date_ref=False, create_type="invoice"):
        contract_obj = self.env["contract.contract"]
        if not date_ref:
            date_ref = fields.Date.context_today(self)
        domain = contract_obj._get_contracts_to_invoice_domain(date_ref)
        domain = expression.AND(
            [
                domain,
                [("generation_type", "=", create_type)],
            ]
        )
        contracts = contract_obj.sudo().search(domain)
        companies = set(contracts.sudo().mapped("company_id"))
        # Invoice by companies, so assignation emails get correct context
        for company in companies:
            contracts_to_invoice = contracts.filtered(
                lambda c: c.company_id == company
                and (not c.date_end or c.recurring_next_date <= c.date_end)
            ).with_company(company)
            self.sudo()._recurring_create_invoice(contracts_to_invoice, date_ref)
        return True

    @api.model
    def _get_contracts_to_invoice_domain(self, date_ref=None):
        """
        This method builds the domain to use to find all
        contracts (contract.contract) to invoice.
        :param date_ref: optional reference date to use instead of today
        :return: list (domain) usable on contract.contract
        """
        domain = []
        if not date_ref:
            date_ref = fields.Date.context_today(self)
        domain.extend([("recurring_next_date", "<=", date_ref)])
        return domain

    @api.model
    def _get_recurring_create_func(self, create_type="invoice"):
        if create_type == "invoice":
            return self.__class__._recurring_create_invoice

    def _recurring_create_invoice(self, contracts_to_invoice, date_ref=False):
        for contract in contracts_to_invoice:
            journal = (
                contract.journal_id
                if contract.journal_id.type == contract.contract_type
                else self.env["account.journal"].search(
                    [
                        ("type", "=", contract.contract_type),
                        ("company_id", "=", contract.company_id.id),
                    ],
                    limit=1,
                )
            )
            if not journal:
                error = _("Please define a %s journal for the company '%s'.") % (
                    contract.contract_type,
                    contract.company_id.name or "",
                )
                contract.sudo().write(
                    {
                        "with_invoice_generation_error": True,
                        "invoice_generation_error": error,
                    }
                )
            else:
                self.sudo()._prepare_recurring_invoices_values(contract, date_ref)

    def _prepare_recurring_invoices_values(self, contracts, date_ref=False):
        for contract in contracts:
            if not date_ref:
                date_ref = contract.recurring_next_date
            if not date_ref:
                # this use case is possible when recurring_create_invoice is
                # called for a finished contract
                continue
            contract_lines = contract.sudo()._get_lines_to_invoice(date_ref)
            if not contract_lines:
                continue
            invoice_vals, move_form = contract.sudo()._prepare_invoice(date_ref)
            invoice_vals["invoice_line_ids"] = []
            for line in contract_lines:
                line.sudo()._prepare_invoice_line_error(move_form=move_form)
