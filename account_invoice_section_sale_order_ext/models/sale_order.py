# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from collections import OrderedDict

from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoice_ids = super()._create_invoices(grouped=grouped, final=final, date=date)
        for invoice in invoice_ids:
            if (
                len(invoice.line_ids.mapped(invoice.line_ids._get_section_grouping()))
                == 1
            ):
                sequence = 10
                move_lines = invoice._get_ordered_invoice_lines()
                # Group move lines according to their sale order
                section_grouping_matrix = OrderedDict()
                for move_line in move_lines:
                    group = move_line._get_section_group()
                    section_grouping_matrix.setdefault(group, []).append(move_line.id)
                section_lines = []
                for group, move_line_ids in section_grouping_matrix.items():
                    if group:
                        section_lines.append(
                            (
                                0,
                                0,
                                {
                                    "name": group._get_invoice_section_name(),
                                    "display_type": "line_section",
                                    "sequence": sequence,
                                    "account_id": False,
                                    "currency_id": invoice.currency_id.id,
                                },
                            )
                        )
                        sequence += 10
                    for move_line in self.env["account.move.line"].browse(
                        move_line_ids
                    ):
                        move_line.sequence = sequence
                        sequence += 10
                invoice.line_ids = section_lines
        return invoice_ids

    def _get_invoice_section_name(self):
        self.ensure_one()
        name = super()._get_invoice_section_name()
        name = _("Order: %(sale_order)s") % {
            "sale_order": name,
        }
        return name
