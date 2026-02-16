from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
    )

    def _sync_employee_to_package(self):
        for line in self:
            package = line.result_package_id or line.package_id
            if line.employee_id and package and package.employee_id != line.employee_id:
                package.employee_id = line.employee_id

    @api.onchange("employee_id", "result_package_id", "package_id")
    def _onchange_employee(self):
        self._sync_employee_to_package()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._sync_employee_to_package()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._sync_employee_to_package()
        return res

    def _action_done(self):
        res = super()._action_done()
        self.exists()._sync_employee_to_package()
        return res
