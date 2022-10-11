# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartnerPermission(models.Model):
    _inherit = 'res.partner.permission'

    is_for_employee = fields.Boolean(
        string="Is for employee", related="type_id.is_for_employee")

    partner_id = fields.Many2one(
        domain=['|',
                ('employee_id', '!=', None),
                ('educational_category', 'in', ('student', 'otherchild'))])

    center_id = fields.Many2one(required=False)
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', related="partner_id.employee_id")

    @api.depends('is_for_employee')
    def _compute_allowed_signer_ids(self):
        super(ResPartnerPermission, self)._compute_allowed_signer_ids()
        for record in self:
            if record.is_for_employee:
                record.allowed_signer_ids = record.partner_id

    def find_or_create_permission(self, partner, center, permission_type):
        if partner.employee_id and not permission_type.is_for_employee:
            return False
        res = super(ResPartnerPermission, self).find_or_create_permission(partner, center, permission_type)
        return res

    @api.model
    def create(self, vals):
        if self.partner_id.employee_id and not self.type_id.is_for_employee:
            raise UserError(_("Unable to create employee type permission to non employee contact."))

        result = super(ResPartnerPermission, self).create(vals)
        return result


