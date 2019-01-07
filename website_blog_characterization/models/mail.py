# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    area_ids = fields.Many2many(
        string='Areas', comodel_name='res.partner.area',
        relation='rel_mass_mailing_area', column1='mass_mailing_id',
        column2='area_id', copy=False)
    post_ids = fields.One2many(
        comodel_name='mail.mass_mailing.blog_post',
        inverse_name='mass_mailing_id', string='Blog Posts')


class MassMailingBlogPost(models.Model):
    _name = 'mail.mass_mailing.blog_post'
    _description = 'Newsletter blog posts'
    _order = 'mass_mailing_id, sequence'

    sequence = fields.Integer(string='Sequence')
    mass_mailing_id = fields.Many2one(
        comodel_name='mail.mass_mailing', string='Mass Mailing')
    post_id = fields.Many2one(
        comodel_name='blog.post', string='Blog Post')
