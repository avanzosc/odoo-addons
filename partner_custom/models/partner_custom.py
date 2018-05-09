# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, _


class ResPartner(models.Model):

    _inherit = 'res.partner'
    comertial_implantation = fields.One2many(commodel_name="res.partner",
                                             string="Comertial implantation")
    productive_implantation = fields.One2many(commodel_name="res.partner",
                                              string="Productive implantation")
    asociated = fields.Many2one(commodel_name="res.partner",
                                string="Asociated")
    asociated_type = fields.Many2one(commodel_name="res.partner",
                                     string="Asociated type")
    nature_entity = fields.Many2one(commodel_name="res.partner",
                                    string="Nature entity")
    high_date = fields.Date("High date")
    low_date = fields.Date("Low date")
    asociated = fields.Selection(
        [('Yes', _('Yes')), ('No', _('No')), ('Asociated potential',
         _('Asociated potential'))], string="Asociated", default="Yes")
    asociated_type = fields.Selection(
        [('Partner', _('Partner')),
         ('Parter/Junior', _('Partner/Junior')), ('Strategic Partner',
         _('Strategic Partner')), ('Strategic Partner Junior',
         _('Strategic Partner Junior'))], string="Asociated type",
        default="Partner")
    nature_entity = fields.Selection(
        [('Company', _('Company')), ('Training center', _('Training center')),
         ('Research center', _('Research center')),
         ('Organism', _('Organism'))], string="Nature of entity",
        default="Company")
    SME = fields.Boolean(default=True, string="SME")
    nature_of_sector = fields.Char(string="Nature of sector")
    group_of_control = fields.Boolean(default=True, string="Group of control")
    doyou = fields.Boolean(default=True, string="Do you have participation of"
                           "NO SMEs or venture capital entities in your"
                           "shareholding?")
    number_of_employees = fields.Integer(string="Number of employees")
    country_id = fields.Many2one(commodel_name="res.country",
                                 string='Select country', select=True)
    comertial_implantation = fields.Many2one(comodel_name='res.partner',
                                             string="Comertial implantation")
    productive_implantation = fields.Many2one(comodel_name='res.partner',
                                              string="Productive implantation")
    date = fields.Date(string="Date")
    real_total_turnover = fields.Integer(string="Real total turnover")
    real_number_employees = fields.Integer(string="Real number of employees")
    real_external_billing = fields.Integer(string="Real external billing")
    real_external_employees_number = fields.Integer(
        string="Real external employees number")
    real_investment_RD = fields.Integer(string="Real investment R & D")
    expected_total_billing = fields.Integer(string="Expected total billing")
    expected_total_employees_number = fields.Integer(
        string="Expected total employees number")
    expected_external_billing = fields.Integer(
        string="Expected external billing")
    expected_external_employees_number = fields.Integer(
        string="Expected external employees number")
    expected_investment_RD = fields.Integer(
        string="Expected investment R & D")
