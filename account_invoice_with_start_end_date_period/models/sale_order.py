# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(
        self, grouped=False, final=False, date=None, start_date=None, end_date=None
    ):
        moves = super(SaleOrder, self)._create_invoices(
            grouped=grouped, final=final, date=date
        )
        if start_date or end_date:
            vals = {
                "start_date_period": start_date or "",
                "end_date_period": end_date or "",
            }
            moves.write(vals)
        else:
            vals = {}
            if ("timesheet_start_date" in self.env.context and
                    self.env.context.get("timesheet_start_date", False)):
                vals["start_date_period"] = (
                    self.env.context.get("timesheet_start_date"))
            if ("timesheet_end_date" in self.env.context and
                    self.env.context.get("timesheet_end_date", False)):
                vals["end_date_period"] = (
                    self.env.context.get("timesheet_end_date"))
            if vals:
                moves.write(vals)
        return moves
