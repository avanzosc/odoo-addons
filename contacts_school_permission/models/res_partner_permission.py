# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartnerPermission(models.Model):
    _name = 'res.partner.permission'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Contact Permission'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Student', required=True,
        domain=[('educational_category', 'in', ('student', 'otherchild'))],
        ondelete="cascade")
    center_id = fields.Many2one(
        comodel_name='res.partner', string='Education Center',
        domain=[('educational_category', 'in', 'school')])
    allowed_signer_ids = fields.Many2many(
        comodel_name='res.partner', string='Allowed Signers',
        compute='_compute_allowed_signer_ids', store=True)
    signer_id = fields.Many2one(
        comodel_name='res.partner', string='Signed by',
        domain="[('id', 'in', allowed_signer_ids)]")
    signer_id_2 = fields.Many2one(
        comodel_name='res.partner', string='Signed by 2',
        domain="[('id', 'in', allowed_signer_ids)]")
    signer_ids = fields.Many2many(
        comodel_name='res.partner', string='Signed by',
        compute="_compute_signer_ids",
        domain="[('id', 'in', allowed_signer_ids)]")
    type_id = fields.Many2one(
        comodel_name='res.partner.permission.type', string='Type',
        required=True)
    type_description = fields.Text(
        string='Type Description', related='type_id.description', store=True)
    description = fields.Text(string='Description')
    state = fields.Selection(
        selection=[('yes', 'Signed'),
                   ('no', 'Refused'),
                   ('pending', 'Pending'),
                   ('conflict', 'Conflict')],
        string='State', default='pending',
        required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    attachment_doc = fields.Binary(string='Attached Document')
    signature = fields.Binary(string='Signature', attachment=True)
    signature_date = fields.Date(string='Signature Date')
    signature_2 = fields.Binary(string='Signature 2', attachment=True)
    signature_date_2 = fields.Date(string='Signature Date 2')
    comments = fields.Text(string="Comments")

    @api.depends('partner_id', 'partner_id.child2_ids',
                 'partner_id.child2_ids.relation',
                 'partner_id.child2_ids.responsible_id')
    def _compute_allowed_signer_ids(self):
        for record in self:
            record.allowed_signer_ids = (
                record.partner_id.child2_ids.filtered(
                    lambda l: l.relation in ('progenitor', 'guardian')
                ).mapped('responsible_id'))

    @api.depends('signature', 'signature_2',
                 'signer_id', 'signer_id_2')
    def _compute_signer_ids(self):
        for record in self:
            if record.signature:
                record.signer_ids |= record.signer_id
            if record.signature_2:
                record.signer_ids |= record.signer_id_2

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s' % (self.type_id.name)

    def find_or_create_permission(self, partner, center, permission_type):
        permission = self.search([
            ("partner_id", "=", partner.id),
            ("center_id", "=", center.id),
            ("type_id", "=", permission_type.id),
        ])
        if not permission:
            permission = self.create({
                "partner_id": partner.id,
                "center_id": center.id,
                "type_id": permission_type.id,
            })
        return permission

    def button_sign(self):
        self.ensure_one()
        self.write({
            'state': 'yes',
            'signer_id': self.env.user.partner_id.id,
        })

    def button_deny(self):
        self.ensure_one()
        self.write({
            'state': 'no',
            'signer_id': self.env.user.partner_id.id,
        })


class ResPartnerPermissionType(models.Model):
    _name = 'res.partner.permission.type'
    _description = 'Permission Type'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    admission_default = fields.Boolean(string='Default in Admission')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    permission_ids = fields.One2many(
        comodel_name='res.partner.permission', inverse_name='partner_id',
        string='Permissions')
