# Copyright 2019 Roberto Lizana - Trey, Jorge Camacho - Trey
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class BlogPost(models.Model):
    _inherit = 'blog.post'

    mailing_ids = fields.Many2many(
        comodel_name='mail.mass_mailing',
        relation='mail_mass_mailing2blog_post_rel',
        column1='post_id',
        column2='mailing_id')
    mailing_included = fields.Boolean(
        compute='_compute_mailing_included',
        store=True,
        string='Mailing Included')
    featured_mailing_ids = fields.Many2many(
        comodel_name='mail.mass_mailing',
        relation='mail_mass_mailing2featured_blog_post_rel',
        column1='post_id',
        column2='mailing_id')

    @api.one
    @api.depends('mailing_ids')
    def _compute_mailing_included(self):
        self.mailing_included = False
        for mailing in self.mailing_ids:
            if mailing.state != 'draft':
                self.mailing_included = True
                break
