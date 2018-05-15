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
        string='Associated', default='yes')
    associated_type = fields.Selection(
        selection=[('partner', 'Partner'),
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
