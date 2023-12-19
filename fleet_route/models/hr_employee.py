# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    contact_info = fields.Char(
        string='Contact Info', compute='_compute_contact_info', store=True)

    @api.multi
    def get_employee_contact_info(self):
        self.ensure_one()
        contact_numbers = []
        contact_numbers += (
            [self.work_phone] if self.work_phone else [])
        contact_numbers += (
            [self.mobile_phone] if self.mobile_phone else [])
        return (
            '/'.join(contact_numbers) if contact_numbers else
            _('Not available'))

    @api.multi
    @api.depends('work_phone', 'mobile_phone')
    def _compute_contact_info(self):
        for employee in self:
            employee.contact_info = employee.get_employee_contact_info()
