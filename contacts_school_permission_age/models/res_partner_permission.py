# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons.contacts_school_permission.models.res_partner_permission import \
    SIGNER_OPTIONS


class ResPartnerPermission(models.Model):
    _inherit = 'res.partner.permission'

    min_age = fields.Integer(related="type_id.min_age")
    signer_id_student = fields.Many2one(
        comodel_name='res.partner', string='Student signed by',
        domain="[('id', 'in', allowed_signer_ids)]")
    signature_student = fields.Binary(string='Signature Student', attachment=True)
    signature_student_status = fields.Selection(
        selection=SIGNER_OPTIONS,
        string='Signature Status',
    )
    signature_student_date = fields.Date(string='Signature Date')

    @api.depends('type_id', 'type_id.min_age',
                 'partner_id', 'partner_id.child2_ids',
                 'partner_id.child2_ids.relation',
                 'partner_id.child2_ids.responsible_id')
    def _compute_allowed_signer_ids(self):
        super(ResPartnerPermission, self)._compute_allowed_signer_ids()
        for record in self:
            if not record.signer_ids:
                if record.min_age and record.partner_id.age >= record.min_age:
                    domain = [
                        ('id', '=', record.partner_id.id)
                    ]
                else:
                    domain = [
                        ('id', 'in', record.partner_id.student_progenitor_ids.ids),
                    ]
                record.allowed_signer_ids = self.env['res.partner'].search(
                    domain
                )

    @api.depends('signature', 'signature_2', 'signature_student')
    def _compute_signer_ids(self):
        super(ResPartnerPermission, self)._compute_signer_ids()
        for record in self:
            if record.signature_student:
                if record.signature_student_status == 'yes':
                    record.signer_ids |= record.signer_id_student
                else:
                    record.refuser_ids |= record.signer_id_student
