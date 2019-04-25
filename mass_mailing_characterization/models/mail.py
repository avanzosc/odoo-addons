# Copyright 2019 Roberto Lizana - Trey, Jorge Camacho - Trey
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api


class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    post_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('done', 'Done')],
        string='Post state',
        default='draft')
    post_ids = fields.Many2many(
        comodel_name='blog.post',
        relation='mail_mass_mailing2blog_post_rel',
        column1='mailing_id',
        column2='post_id')
    post_line_ids = fields.One2many(
        comodel_name='mail.mass_mailing.post_line',
        inverse_name='mailing_id',
        string='Posts')
    featured_post_ids = fields.Many2many(
        comodel_name='blog.post',
        relation='mail_mass_mailing2featured_blog_post_rel',
        column1='mailing_id',
        column2='post_id')

    @api.multi
    def action_post_state_draft(self):
        self.post_state = 'draft'

    @api.multi
    def action_post_state_done(self):
        post_exists_ids = [l.post_id.id for l in self.post_line_ids]
        to_create = [p for p in self.post_ids if p.id not in post_exists_ids]
        for post in to_create:
            self.env['mail.mass_mailing.post_line'].create({
                'mailing_id': self.id,
                'post_id': post.id,
                'sequence': 10})
        to_delete = [
            p for p in self.post_line_ids
            if p.post_id.id not in self.post_ids.ids]
        for post in to_delete:
            post.unlink()
        self.post_state = 'done'

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        new = super().copy(default=default)
        new.action_post_state_draft()
        new.action_post_state_done()
        return new

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        record = super().create(vals)
        record.action_post_state_draft()
        record.action_post_state_done()
        return record


class MassMailingPostLine(models.Model):
    _name = 'mail.mass_mailing.post_line'
    _order = 'sequence asc'

    sequence = fields.Integer(
        string='Sequence')
    post_id = fields.Many2one(
        comodel_name='blog.post',
        string='Post')
    area_ids = fields.Many2many(
        related='post_id.area_ids',
        readonly=True)
    mailing_id = fields.Many2one(
        comodel_name='mail.mass_mailing',
        string='LABEL')
