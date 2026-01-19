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
            if line.employee_id and line.package_id:
                line.package_id.employee_id = line.employee_id

    def _action_done(self):

        res = super()._action_done()
        for line in self.exists():
            if line.employee_id and line.package_id and not line.package_id.employee_id:
                line.package_id.employee_id = line.employee_id
        return res
