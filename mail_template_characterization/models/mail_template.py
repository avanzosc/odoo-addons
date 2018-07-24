# Copyright 2018 Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class MailTemplate(models.Model):
    "Templates for sending email"
    _inherit = 'mail.template'

    area_ids = fields.Many2many(
        string='Areas', comodel_name='res.partner.area',
        relation='rel_mail_template_area', column1='mail_template_id',
        column2='area_id', copy=False)
    committee_ids = fields.Many2many(
        string='Committees', comodel_name='res.committee',
        relation='rel_mail_template_committee', column1='mail_template_id',
        column2='committee_id', copy=False)
    team_ids = fields.Many2many(
        string='Teams', comodel_name='res.team',
        relation='rel_mail_template_team', column1='mail_template_id',
        column2='team_id', copy=False)
    structure_ids = fields.Many2many(
        string='Structures', comodel_name='res.structure',
        relation='rel_mail_template_structure', column1='mail_template_id',
        column2='structure_id', copy=False)
    main_contact = fields.Boolean(string='Main Contact')
    assembly = fields.Boolean(string='Assembly')
    joint = fields.Boolean(string='Joint')
    bidding = fields.Boolean(string='Bidding')
