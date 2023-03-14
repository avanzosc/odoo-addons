# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    print_discount = fields.Boolean(
        string="Print discount", compute="_compute_print_discounts"
    )
    print_discount2 = fields.Boolean(
        string="Print discount 2", compute="_compute_print_discounts"
    )
    print_discount3 = fields.Boolean(
        string="Print discount 3", compute="_compute_print_discounts"
    )

    def _compute_print_discounts(self):
        for invoice in self:
            discount = False
            discount2 = False
            discount3 = False
            lines = invoice.invoice_line_ids.filtered(lambda x: x.discount)
            if lines:
                discount = True
            lines = invoice.invoice_line_ids.filtered(lambda x: x.discount2)
            if lines:
                discount2 = True
            lines = invoice.invoice_line_ids.filtered(lambda x: x.discount3)
            if lines:
                discount3 = True
            invoice.print_discount = discount
            invoice.print_discount2 = discount2
            invoice.print_discount3 = discount3
