# Copyright 2018 Gotzon Imaz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class BlogPost(models.Model):
    _inherit = 'blog.post'

    area_ids = fields.Many2many(
        string='Areas', comodel_name='res.partner.area',
        relation='rel_blog_area', column1='blog_id',
        column2='area_id', copy=False)
    committee_ids = fields.Many2many(
        string='Committees', comodel_name='res.committee',
        relation='rel_blog_committee', column1='blog_id',
        column2='committee_id', copy=False)
    team_ids = fields.Many2many(
        string='Teams', comodel_name='res.team',
        relation='rel_blog_team', column1='blog_id',
        column2='team_id', copy=False)
    structure_ids = fields.Many2many(
        string='Structures', comodel_name='res.structure',
        relation='rel_blog_structure', column1='blog_id',
        column2='structure_id', copy=False)
    main_contact = fields.Boolean(string='Main Contact')
    assembly = fields.Boolean(string='Assembly')
    joint = fields.Boolean(string='Joint')
    bidding = fields.Boolean(string='Bidding')
