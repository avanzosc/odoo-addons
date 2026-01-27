from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
    )

    @api.onchange("employee_id")
    def _onchange_employee(self):
        for line in self:
            package = line.result_package_id or line.package_id
            if line.employee_id and package:
                package.employee_id = line.employee_id

    def _action_done(self):
        res = super()._action_done()
        for line in self.exists():
            package = line.result_package_id or line.package_id
            if line.employee_id and package:
                package.employee_id = line.employee_id
        return res

