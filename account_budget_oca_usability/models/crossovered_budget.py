# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class CrossoveredBudget(models.Model):
    _inherit = "crossovered.budget"

    def button_recompute_practical_amount(self):
        fnames = ["practical_amount"]
        lines = self.mapped("crossovered_budget_line_ids")
        for fname in fnames:
            self.env.add_to_compute(lines._fields[fname], lines)
        lines.modified(fnames)
