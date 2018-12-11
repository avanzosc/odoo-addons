# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerSuccessStory(models.Model):
    _name = 'res.partner.success_story'
    _description = 'Success Story'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner', required=True,
        ondelete='cascade')
    solution_description = fields.Text(
        string='General description of the solution')
    services_description = fields.Text(
        string='Outstanding services and components (maximum 5 units)')
    company_description = fields.Text(
        string='Description of the demonstrator that tells the success story '
               'provided by the company')
    challenge_proposal = fields.Text(
        string='Proposal of challenges attended')
    story_partner_id = fields.Many2one(
        comodel_name='res.partner', string='Success Story Partner',
        domain="[('is_company','=',True)]")
    story_partner_industry_id = fields.Many2one(
        comodel_name='res.partner.industry', string='Industry',
        related='story_partner_id.industry_id', store=True)
    story_contact_id = fields.Many2one(
        comodel_name='res.partner', string='Contact',
        domain="[('parent_id','!=',False),('parent_id','=',story_partner_id),"
               "('type','=','contact')]")
    story_contact_email = fields.Char(
        string='Email', related='story_contact_id.email', store=True)
    profit_ids = fields.One2many(
        comodel_name='res.partner.success_story.profit',
        inverse_name='story_id', string='Profits')
    cost = fields.Selection(
        selection=[(1, '< 20.000'),
                   (2, '20.000 - 50.000'),
                   (3, '50.000 - 100.000'),
                   (4, '100.000 - 250.000'),
                   (5, '> 250.000')], string='Cost of the Solution')
    customer_size = fields.Selection(
        selection=[(1, '< 500.000'),
                   (2, '500.000 - 1.000.000'),
                   (3, '1.000.000 - 5.000.000'),
                   (4, '> 5.000.000')], string='Customer Size')


class ResPartnerSuccessStoryProfit(models.Model):
    _name = 'res.partner.success_story.profit'
    _description = 'Success Story Profit'

    story_id = fields.Many2one(
        comodel_name='res.partner.success_story', string='Success Story',
        required=True, ondelete='cascade')
    name = fields.Char(string='Term / Profit', required=True)
    description = fields.Text(string='Brief Description of the Profit')
