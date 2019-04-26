# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

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
        inverse_name='family_id', string='Families')
    family = fields.Char(string='Family', readonly="1")
    old_student = fields.Boolean(string='Old student', default=False)
    employee_id = fields.Many2one(
        string='Related Employee', comodel_name='hr.employee',
        compute='_compute_employee', store=True)
    employee = fields.Boolean(compute='_compute_employee', store=True)
    student_characteristic_ids = fields.One2many(
        comodel_name='res.partner.student.characteristic',
        inverse_name='student_id', string='Student Characteristics')

    @api.model
    def create(self, vals):
        if vals.get('educational_category') == 'family':
            vals.update({
                'family': (self.env['ir.sequence'].next_by_code(
                    'res.partner.family') or _('New'))
            })
        return super(ResPartner, self).create(vals)

    @api.depends('user_ids', 'user_ids.employee_ids')
    def _compute_employee(self):
        for record in self:
            record.employee_id = record.mapped('user_ids.employee_ids')[:1]
            record.employee = bool(record.employee_id)

    @api.constrains('child2_ids')
    def _check_payers_percentage(self):
        for record in self.filtered('child2_ids'):
            if sum(record.child2_ids.filtered('payer').mapped(
                    'payment_percentage')) != 100.0:
                raise ValidationError(
                    _('The sum of payers percentage must be 100.0'))

    @api.multi
    def check_payer_is_company(self):
        for record in self.filtered(lambda l: l.educational_category in (
                'progenitor', 'guardian', 'otherrelative')):
            record.company_type = ('company' if any(record.mapped(
                'responsible_ids.payer')) else record.company_type or 'person')


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
        string='Student', comodel_name='res.partner', required=True,
        domain=[('educational_category', 'in', ('student', 'other'))])
    child2_educational_category = fields.Selection(
        string='Student Educational Category',
        related='child2_id.educational_category', store=True)
    responsible_id = fields.Many2one(
        string='Responsible', comodel_name='res.partner', required=True,
        domain=[('educational_category', 'in',
                 ('progenitor', 'guardian', 'otherrelative'))])
    responsible_company_type = fields.Selection(
        string='Company Type', related='responsible_id.company_type',
        store=True)
    responsible_educational_category = fields.Selection(
        string='Responsible educational category',
        related='responsible_id.educational_category', store=True)
    responsible_old_student = fields.Boolean(
        string='Responsible old student', related='responsible_id.old_student',
        store=True)
    relation = fields.Selection(
        string='Relation',
        selection=[('progenitor', 'Progenitor'),
                   ('guardian', 'Legal Guardian'),
                   ('otherrelative', 'Other relative')])
    family_id = fields.Many2one(
        string='Family', comodel_name='res.partner', required=True,
        domain=[('educational_category', '=', 'family')])
    family_educational_category = fields.Selection(
        string='Family educational category',
        related='family_id.educational_category', store=True)
    family_old_student = fields.Boolean(
        string='Family old student', related='family_id.old_student',
        store=True)
    payer = fields.Boolean(string='Is Payer?')
    payment_percentage = fields.Float(string='Percentage', default=100.0)
    payment_mode_id = fields.Many2one(
        string='Payment Mode', comodel_name='account.payment.mode',
        store=True, related='responsible_id.customer_payment_mode_id',
        company_dependent=True)
    bank_id = fields.Many2one(
        string='Bank', comodel_name='res.partner.bank',
        domain="[('partner_id', '=', responsible_id)]")

    _sql_constraints = [
        ('relation_unique', 'unique(child2_id,responsible_id,family_id)',
         'Only one type of relation per student, relative and family!'),
    ]

    @api.model
    def create(self, values):
        result = super(ResPartnerFamily, self).create(values)
        if result.responsible_id:
            result.responsible_id.check_payer_is_company()
        return result

    @api.multi
    def write(self, values):
        result = super(ResPartnerFamily, self).write(values)
        if 'payer' in values or 'responsible_id' in values:
            self.mapped('responsible_id').check_payer_is_company()
        return result

    @api.constrains('payment_percentage')
    def _check_payment_percentage(self):
        for record in self.filtered('payer'):
            if (record.payment_percentage <= 0.0 or
                    record.payment_percentage > 100.0):
                raise ValidationError(
                    _("Percentage should be between 0.0 and 100.0"))

    @api.onchange('responsible_id', 'payer')
    def onchange_responsible_id(self):
        if self.responsible_id.bank_ids:
            self.bank_id = (self.responsible_id.bank_ids.filtered(
                lambda c: c.use_default)[:1] or
                self.responsible_id.bank_ids[:1])


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
        string='Student', comodel_name='res.partner', required=True,
        domain=[('educational_category', '=', 'student')])
    information_id = fields.Many2one(
        string='Information', comodel_name='res.partner.information')
    type_id = fields.Many2one(
        string='Information type',
        comodel_name='res.partner.information.type',
        related='information_id.type_id', store=True)
    observations = fields.Text(string='Observations')
    dop_id = fields.Many2one(
        string='DOP', comodel_name='res.partner',
        domain=[('employee', '=', True)])


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    use_default = fields.Boolean(string='Use by default', default=False)
