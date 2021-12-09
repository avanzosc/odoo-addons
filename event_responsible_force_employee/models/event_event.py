# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    allowed_employee_ids = fields.Many2many(
        comodel_name="res.users", string="Allowed employees",
        compute="_compute_allowed_employee_ids")

    def _compute_allowed_employee_ids(self):
        cond = [('company_id', '=', self.company_id.id),
                ('user_id', '!=', False),
                ('user_id.company_id', '=', self.company_id.id)]
        employees = self.env['hr.employee'].search(cond)
        self.allowed_employee_ids = [(6, 0, employees.mapped('user_id').ids)]
