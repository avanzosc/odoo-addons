# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tools.safe_eval import safe_eval
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class MassMailingPost(models.TransientModel):
    _name = 'mail.mass_mailing.post'

    mailing_id = fields.Many2one(comodel_name='mail.mass_mailing')
    post_ids = fields.One2many(
        comodel_name='mail.mass_mailing.post.line', inverse_name='wizard_id',
        required=True)

    @api.model
    def default_get(self, fields):
        res = super(MassMailingPost, self).default_get(fields)
        context = self.env.context or {}
        if context.get('active_model') == 'mail.mass_mailing':
            if len(context.get('active_ids')) > 1:
                raise UserError(_('You must select only one mass mailing.'))
            res.update({
                'mailing_id': context.get('active_id'),
            })
        if context.get('active_model') == 'blog.post':
            post_ids = []
            sequence = 0
            for post_id in context.get('active_ids'):
                post_ids.append((0, 0, {
                    'sequence': sequence,
                    'post_id': post_id,
                }))
                sequence += 1
            res.update({
                'post_ids': post_ids,
            })
        return res

    @api.multi
    def assign_blog_posts(self):
        mailing_post_model = self.env['mail.mass_mailing.blog_post']
        for wizard in self:
            if not wizard.mailing_id:
                wizard.mailing_id = wizard.mailing_id.create({
                    'name': 'FROGA',
                })
            for line in wizard.post_ids:
                mailing_post_model.create({
                    'mass_mailing_id': wizard.mailing_id.id,
                    'post_id': line.post_id.id,
                    'sequence': line.sequence,
                })
        action = self.env.ref('mass_mailing.action_view_mass_mailings')
        action_dict = action.read()[0] if action else {}
        new_domain = [('id', '=', self.mapped('mailing_id').ids)]
        action_dict['domain'] = expression.AND(
            [new_domain, safe_eval(action_dict.get('domain') or '[]')])
        return action_dict


class MassMailingPostLine(models.TransientModel):
    _name = 'mail.mass_mailing.post.line'

    wizard_id = fields.Many2one(comodel_name='mail.mass_mailing.post')
    sequence = fields.Integer(string='Sequence')
    post_id = fields.Many2one(comodel_name='blog.post')
