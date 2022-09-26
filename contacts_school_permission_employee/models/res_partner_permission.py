# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons.contacts_school_permission.models.res_partner_permission import \
    SIGNER_OPTIONS


class ResPartnerPermission(models.Model):
    _inherit = 'res.partner.permission'

    is_for_employee = fields.Boolean(
        string="Is for employee", related="type_id.is_for_employee")

    partner_id = fields.Many2one(
        domain=['|',
                ('employee_id', '!=', None),
                ('educational_category', 'in', ('student', 'otherchild'))])

    @api.depends('allowed_signer_ids')
    def _compute_allowed_signer_ids(self):
        super(ResPartnerPermission, self)._compute_allowed_signer_ids()
        for record in self:
            if record.is_for_employee:
                record.allowed_signer_ids = record.partner_id