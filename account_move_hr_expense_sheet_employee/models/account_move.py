# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    hr_expense_sheet_ids = fields.One2many(
        string="",
        comodel_name="hr.expense.sheet",
        inverse_name="account_move_id",
        copy=False,
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        copy=False,
        store=True,
        compute="_compute_employee_id",
    )

    @api.depends("hr_expense_sheet_ids", "hr_expense_sheet_ids.employee_id")
    def _compute_employee_id(self):
        for move in self:
            employee = False
            if move.hr_expense_sheet_ids:
                expenses = move.hr_expense_sheet_ids.filtered(lambda x: x.employee_id)
                if expenses:
                    employee = expenses.mapped("employee_id")
                    employee = employee.id
            move.employee_id = employee
