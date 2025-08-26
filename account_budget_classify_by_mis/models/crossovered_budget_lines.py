# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    mis_report_template_id = fields.Many2one(
        string="Mis Report Template", comodel_name="mis.report", copy=False
    )
    mis_report_kpi_id = fields.Many2one(
        string="MIS Report KPI", comodel_name="mis.report.kpi", copy=False
    )
