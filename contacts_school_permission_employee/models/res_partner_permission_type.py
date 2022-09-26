
from odoo import api, fields, models


class ResPartnerPermissionType(models.Model):
    _inherit = 'res.partner.permission.type'

    is_for_employee = fields.Boolean(string="Is for employee")

    @api.onchange('is_for_employee')
    def onchange_is_for_employee(self):
        for record in self:
            if record.is_for_employee:
                record.sign_both = False
                record.cannot_cancel = True
