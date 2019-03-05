# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    educational_category = fields.Selection(
        string='Educational category', required=True,
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
                   ('otherfamily', 'Other family')])
    assoc_fede_ids = fields.One2many(
        comodel_name='res.partner.association.federation',
        inverse_name='parent_partner_id', string='Association/Federation')
    family_ids = fields.Many2many(
        comodel_name='res.partner.family',
        relation='rel_partner_family', column1='partner_id',
        column2='family_id', string='Family')
    family = fields.Char(string='Family', readonly="1")
    old_student = fields.Boolean(string='Old student', default=False)

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)
        if (partner.educational_category and
                partner.educational_category == 'family'):
            partner.family = (
                self.env['ir.sequence'].next_by_code('res.partner.family') or
                _('New'))
        return partner


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
    _rec_name = 'partner_id'

    partner_id = fields.Many2one(
        string='Partner', comodel_name='res.partner',
        required=True)
    educational_category = fields.Selection(
        string='Educational category',
        related='partner_id.educational_category')
    family = fields.Char(string='Family', related='partner_id.family')
    old_student = fields.Boolean(
        string='Old student', related='partner_id.old_student')
