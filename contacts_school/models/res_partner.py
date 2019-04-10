# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _default_employee_id(self):
        cond = [('user_id', '=', self.env.user.id)]
        employee = self.env['hr.employee'].search(cond, limit=1)
        return employee.id if employee else False

    educational_category = fields.Selection(
        string='Educational category',
        selection=[('federation', 'Federation'),
                   ('association', 'Association'),
                   ('school', 'School'),
                   ('family', 'Family'),
                   ('student', 'Student'),
                   ('progenitor', 'Progenitor'),
                   ('guardian', 'legal guardian'),
                   ('other', 'Other children'),
                   ('pedagogical', 'Pedagogical company'),
                   ('related', 'Related partner'),
                   ('otherrelative', 'Other relative')])
    assoc_fede_ids = fields.One2many(
        comodel_name='res.partner.association.federation',
        inverse_name='parent_partner_id', string='Association/Federation')
    child2_ids = fields.One2many(
        comodel_name='res.partner.family',
        inverse_name='child2_id', string='Children')
    responsible_ids = fields.One2many(
        comodel_name='res.partner.family',
        inverse_name='responsible_id', string='Responsibles')
    family_ids = fields.One2many(
        comodel_name='res.partner.family',
        inverse_name='family_id', string='Familys')
    family = fields.Char(string='Family', readonly="1")
    old_student = fields.Boolean(string='Old student', default=False)
    employee_id = fields.Many2one(
        string='Employee', comodel_name='hr.employee',
        default=_default_employee_id)
    student_characteristic_ids = fields.One2many(
        comodel_name='res.partner.student.characteristic',
        inverse_name='student_id', string='Student Characteristics')
    payer_ids = fields.One2many(
        comodel_name='res.partner.student.payer',
        inverse_name='student_id', string='Payers')

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)
        if (partner.educational_category and
                partner.educational_category == 'family'):
            partner.family = (
                self.env['ir.sequence'].next_by_code('res.partner.family') or
                _('New'))
        return partner

    @api.constrains('payer_ids', 'payer_ids.percentage')
    def _check_payer_percentage(self):
        if self.payer_ids:
            total = sum(self.payer_ids.mapped('percentage'))
            if total != 100.00:
                raise ValidationError(
                    'The sum of percentages of the payers must be 100%')


class ResPartnerAssociationFederation(models.Model):
    _name = 'res.partner.association.federation'
    _description = 'Partner associations, and federations.'

    parent_partner_id = fields.Many2one(
        string='Partner parent', comodel_name='res.partner',
        required=True)
    partner_id = fields.Many2one(
        string='Association/Federation', comodel_name='res.partner',
        required=True)
    education_category = fields.Selection(
        string='Educational category', store=True,
        related='partner_id.educational_category')
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date')
    notes = fields.Text(string="Notes")


class ResPartnerFamily(models.Model):
    _name = 'res.partner.family'
    _description = 'Partner family.'
    _rec_name = 'child2_id'

    child2_id = fields.Many2one(
        string='Child', comodel_name='res.partner')
    child2_educational_category = fields.Selection(
        selection=[('student', 'Student'),
                   ('other', 'Other children')],
        string='Child educational category',
        related='child2_id.educational_category', store=True)
    child2_old_student = fields.Boolean(
        string='Child old student', related='child2_id.old_student',
        store=True)
    responsible_id = fields.Many2one(
        string='Responsible', comodel_name='res.partner', store=True)
    responsible_educational_category = fields.Selection(
        selection=[('progenitor', 'Progenitor'),
                   ('guardian', 'legal guardian'),
                   ('otherrelative', 'Other relative')],
        string='Responsible educational category',
        related='responsible_id.educational_category', store=True)
    responsible_old_student = fields.Boolean(
        string='Responsible old student', related='responsible_id.old_student',
        store=True)
    relation = fields.Selection(
        string='Relation',
        selection=[('progenitor', 'Progenitor'),
                   ('guardian', 'legal guardian'),
                   ('otherrelative', 'Other relative')])
    family_id = fields.Many2one(
        string='Family', comodel_name='res.partner')
    family_educational_category = fields.Selection(
        selection=[('family', 'Family')],
        string='Family educational category',
        related='family_id.educational_category', store=True)
    family_old_student = fields.Boolean(
        string='Family old student', related='family_id.old_student',
        store=True)


class ResPartnerInformationType(models.Model):
    _name = 'res.partner.information.type'
    _description = 'Partner information type.'

    name = fields.Char(
        string='Description', required=True)


class ResPartnerInformation(models.Model):
    _name = 'res.partner.information'
    _description = 'Partner information.'

    name = fields.Char(
        string='Description', required=True)
    type_id = fields.Many2one(
        string='Information type',
        comodel_name='res.partner.information.type')


class ResPartnerStudentCharacteristic(models.Model):
    _name = 'res.partner.student.characteristic'
    _description = 'Student characteristic.'
    _rec_name = 'information_id'

    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner', required=True)
    information_id = fields.Many2one(
        string='Information', comodel_name='res.partner.information')
    type_id = fields.Many2one(
        string='Information type',
        comodel_name='res.partner.information.type',
        related='information_id.type_id', store=True)
    observations = fields.Text(string='Observations')
    dop_id = fields.Many2one(
        string='DOP', comodel_name='res.partner')


class ResPartnerStudentPayer(models.Model):
    _name = 'res.partner.student.payer'
    _description = 'Student payers.'
    _rec_name = 'partner_id'

    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner', required=True)
    partner_id = fields.Many2one(
        string='Payer', comodel_name='res.partner')
    education_category = fields.Selection(
        string='Educational category', store=True,
        related='partner_id.educational_category')
    percentage = fields.Float(
        string='Percentage', required=True, default=100.0)
    allowed_family_ids = fields.Many2many(
        comodel_name='res.partner')
    payment_term_id = fields.Many2one(
        string='Payment Terms', comodel_name='account.payment.term',
        store=True, related='partner_id.property_supplier_payment_term_id')
    bank_id = fields.Many2one(
        string='Bank', comodel_name='res.partner.bank')

    @api.onchange('student_id')
    def onchange_student_id(self):
        if self.student_id.family_ids:
            partners = self.env['res.partner']
            partners += self.student_id.family_ids.mapped('responsible_id')
            partners += self.student_id.family_ids.mapped('family_id')
            self.allowed_family_ids = [(6, 0, partners.ids)]

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id and self.partner_id.bank_ids:
            bank = self.partner_id.bank_ids.filtered(lambda c: c.use_default)
            if not bank:
                bank = self.partner_id.bank_ids[0]
            if bank:
                self.bank_id = bank.id


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    use_default = fields.Boolean(string='Use by default', default=False)
