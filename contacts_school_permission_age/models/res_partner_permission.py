# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartnerPermission(models.Model):
    _inherit = 'res.partner.permission'

    min_age = fields.Integer(related="type_id.min_age")
    signer_id_student = fields.Many2one(
        comodel_name='res.partner', string='Student signed by',
        domain="[('id', 'in', allowed_signer_ids)]")
    signature_student = fields.Binary(string='Signature Student', attachment=True)
    signature_student_status = fields.Selection(
        selection=[('yes', 'Signed'),
                   ('no', 'Refused')],
        string='Signature Status', default="")
    signature_student_date = fields.Date(string='Signature Date')

    @api.depends('partner_id', 'partner_id.child2_ids',
                 'partner_id.child2_ids.relation',
                 'partner_id.child2_ids.responsible_id')
    def _compute_allowed_signer_ids(self):
        super(ResPartnerPermission, self)._compute_allowed_signer_ids()
        for record in self:
            record._compute_allowed_student_ids()

    @api.onchange('type_id')
    def _compute_allowed_student_ids(self):
        self.ensure_one()
        if self.min_age and self.partner_id.age >= self.min_age:
            domain = [
                ('id', '=', self.partner_id.id)
            ]
        else:
            domain = [
                ('id', 'in', self.partner_id.student_progenitor_ids.ids),
            ]
        self.allowed_signer_ids = self.env['res.partner'].search(
            domain
        )

    def _compute_signer_ids(self):
        super(ResPartnerPermission, self)._compute_signer_ids()
        for record in self:
            signer_ids = refuser_ids = self.env["res.partner"]
            if record.signature_student_date:
                if record.signature_student_status == 'yes':
                    signer_ids |= record.signer_id_student
                else:
                    refuser_ids |= record.signer_id_student
            if signer_ids and refuser_ids:
                state = "conflict"
            elif signer_ids and not refuser_ids:
                state = "yes"
            elif not signer_ids and refuser_ids:
                state = "no"
            else:
                state = "pending"
            record.signer_ids = signer_ids
            record.refuser_ids = refuser_ids
            record.state = state
