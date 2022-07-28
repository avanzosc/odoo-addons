# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_data_for_create_analytic_line(self):
        self.ensure_one()
        vals = super(StockMove, self)._prepare_data_for_create_analytic_line()
        if self.picking_id.task_id:
            vals.update(
                {
                    "task_id": self.picking_id.task_id.id,
                    "project_id": False,  # this is an analytic line not a timesheet
                }
            )
        return vals
