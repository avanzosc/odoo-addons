# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    commercial_country_ids = fields.Many2many(
        comodel_name='res.country', relation='rel_commmercial_countries',
        column1='partner_id', column2='country_id',
        string='Commercial Interest Countries')
    commercial_imp_ids = fields.Many2many(
        comodel_name='res.partner', relation='rel_commercial_implatation',
        column1='partner_id', column2='commercial_imp_id',
        string='Commercial Implantation')
    productive_imp_ids = fields.Many2many(
        comodel_name='res.partner', relation='rel_productive_implatation',
        column1='partner_id', column2='productive_imp_id',
        string='Productive Implantation')
    subscription_date = fields.Date(string='Subscription Date')
    unsubscription_date = fields.Date(string='Unsubscription Date')
    associated = fields.Selection(
        selection=[('yes', 'Yes'),
                   ('no', 'No'),
                   ('potential', 'Associated potential')],
        string='Associated', default='no')
    associated_type = fields.Selection(
        selection=[('partner', 'Associate'),
                   ('junior', 'Partner/Junior'),
                   ('strategic', 'Strategic Partner'),
                   ('strategic_junior', 'Strategic Partner Junior')],
        string='Associated Type', default='partner')
    entity_character = fields.Selection(
        selection=[('company', 'Company'),
                   ('training_center', 'Training center'),
                   ('research_center', 'Research center'),
                   ('organism', 'Organism')],
        string='Entity Character', default='company')
    sme_business = fields.Boolean(default=True, string='SME')
    sector_character = fields.Many2one(
        comodel_name='res.character', string='Sector Character')
    group_of_control = fields.Boolean(default=True, string='Group of control')
    have_participation = fields.Boolean(
        string='Do you have participation of NO SMEs or venture capital'
        'entities in your shareholding?')
    number_of_employees = fields.Integer(string='Number of employees')
    economic_data_ids = fields.One2many(
        comodel_name='res.partner.economic_data', inverse_name='partner_id',
        string='Economic Data')
    economic_date = fields.Date(string='Economic Data Date')
    real_total_turnover = fields.Integer(string='Real total turnover')
    real_number_employees = fields.Integer(string='Real number of employees')
    real_external_billing = fields.Integer(string='Real external billing')
    real_external_employees_number = fields.Integer(
        string='Real external employees number')
    real_investment_RD = fields.Integer(string='Real investment R & D')
    expected_total_billing = fields.Integer(string='Expected total billing')
    expected_total_employees_number = fields.Integer(
        string='Expected total employees number')
    expected_external_billing = fields.Integer(
        string='Expected external billing')
    expected_external_employees_number = fields.Integer(
        string='Expected external employees number')
    expected_investment_RD = fields.Integer(
        string='Expected investment R & D')
    activity_id = fields.Many2one(
        string='Activity', comodel_name='res.activity', copy=False)
    activity_type_ids = fields.Many2many(
        string='Activity Types', comodel_name='res.activity.type',
        relation='rel_partner_activity_type', column1='partner_id',
        column2='type_id', copy=False)
    specialization_ids = fields.Many2many(
        string='Specializations', comodel_name='res.area.specialization',
        relation='rel_partner_specialization', column1='partner_id',
        column2='specialization_id', copy=False)
    area_ids = fields.Many2many(
        string='Areas', comodel_name='res.partner.area',
        relation='rel_partner_area', column1='partner_id',
        column2='area_id', copy=False)
    committee_ids = fields.Many2many(
        string='Committees', comodel_name='res.committee',
        relation='rel_partner_committee', column1='partner_id',
        column2='committee_id', copy=False)
    team_ids = fields.Many2many(
        string='Teams', comodel_name='res.team',
        relation='rel_partner_team', column1='partner_id',
        column2='team_id', copy=False)
    structure_ids = fields.Many2many(
        string='Structures', comodel_name='res.structure',
        relation='rel_partner_structure', column1='partner_id',
        column2='structure_id', copy=False)
    main_contact = fields.Boolean(string='Main Contact')
    assembly = fields.Boolean(string='Assembly')
    joint = fields.Boolean(string='Joint')
    bidding = fields.Boolean(string='Bidding')
    foundation_year = fields.Integer(string='Foundation Year')
    incorporate_user_id = fields.Many2one(
        comodel_name='res.users', string='Incorporate EE',
        domain="[('employee_ids', '!=', False)]")
    interlocutor_user_id = fields.Many2one(
        comodel_name='res.users', string='Interlocutor EE',
        domain="[('employee_ids', '!=', False)]")


class ResPartnerEconomicdata(models.Model):
    _name = 'res.partner.economic_data'
    _description = 'Economic Data from Partner'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    economic_date = fields.Date(string='Economic Data Date', required=True)
    real_total_turnover = fields.Float(string='Real total turnover')
    real_number_employees = fields.Integer(string='Real number of employees')
    real_external_billing = fields.Integer(string='Real external billing')
    real_external_employees_number = fields.Integer(
        string='Real external employees number')
    real_investment_RD = fields.Integer(string='Real investment R & D')
    expected_total_billing = fields.Integer(string='Expected total billing')
    expected_total_employees_number = fields.Integer(
        string='Expected total employees number')
    expected_external_billing = fields.Integer(
        string='Expected external billing')
    expected_external_employees_number = fields.Integer(
        string='Expected external employees number')
    expected_investment_RD = fields.Integer(
        string='Expected investment R & D')
