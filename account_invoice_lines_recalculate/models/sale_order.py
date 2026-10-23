# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_invoiceable_lines(self, final=False):
        lines = super()._get_invoiceable_lines(final=final)
        if any(line._is_discount_base_line() for line in lines):
            lines |= self.order_line.filtered(
                lambda line: line._is_recalculate_discount_line()
            )
        return lines

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super()._create_invoices(grouped=grouped, final=final, date=date)
        discount_lines = invoices.invoice_line_ids.filtered(
            lambda line: (
                line.product_id.discount_percentage
                and line.product_id.categ_id.discounts_exclude
            )
        )
        discount_lines.recalculate_invoice_line()
        return invoices


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _is_recalculate_discount_line(self):
        self.ensure_one()
        return bool(
            not self.display_type
            and self.product_id.discount_percentage
            and self.product_id.categ_id.discounts_exclude
        )

    def _is_discount_base_line(self):
        self.ensure_one()
        return bool(
            not self.display_type
            and not self.product_id.discount_percentage
            and not self.product_id.categ_id.discounts_exclude
        )

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        if not self._is_recalculate_discount_line():
            return super()._prepare_invoice_line(**optional_values)
        return super()._prepare_invoice_line(quantity=1.0, **optional_values)
