# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    is_repair = fields.Boolean(
        string="Is repair", compute="_compute_is_repair")
    amount_total_products_rmas = fields.Monetary(
        string="Amount repair orders", currency_field='currency_id',
        compute="_compute_amount_total_products_rmas")

    def _compute_is_repair(self):
        for invoice in self:
            lines = invoice.invoice_line_ids.filtered(
                lambda x: x.sale_line_id and x.sale_line_id.is_repair)
            invoice.is_repair = True if lines else False

    def _compute_amount_total_products_rmas(self):
        for invoice in self:
            if not invoice.is_repair:
                invoice.amount_total_products_rmas = 0
            else:
                amount_total_products_rmas = 0
                for line in invoice.line_ids:
                    if line.amount_products_rmas:
                        amount_total_products_rmas += line.amount_products_rmas
                invoice.amount_total_products_rmas = amount_total_products_rmas
