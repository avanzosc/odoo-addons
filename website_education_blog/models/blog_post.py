
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class BlogPost(models.Model):
    _inherit = "blog.post"

    blog_education_center_ids = fields.Many2many(
        related="blog_id.education_center_ids")
    blog_education_course_ids = fields.Many2many(
        related="blog_id.education_course_ids")
    blog_education_group_ids = fields.Many2many(
        related="blog_id.education_group_ids")
    blog_education_category_ids = fields.Char(
        related="blog_id.education_category_ids")

    education_center_ids = fields.Many2many(
        string='Education Centers',
        comodel_name="res.partner",
        relation='post_center_rel',
        column1='post_id',
        column2='center_id', store=True)
    education_course_ids = fields.Many2many(
        string='Education Courses', comodel_name="education.course", store=True)
    education_group_ids = fields.Many2many(
        string='Education Groups', comodel_name="education.group", store=True)
    education_category_ids = fields.Char(
        string='Educational Category')

    invited_partner_ids = fields.Many2many(
        string='Invited Partners', comodel_name="res.partner",
        compute="_compute_invited_partners"
    )
    invited_count = fields.Integer(
        'Count Invited People', compute="_compute_count_invited_partners")

    @api.model
    def create(self, vals):
        post_id = super(BlogPost, self).create(vals)
        post_id.education_center_ids = post_id.blog_id.education_center_ids
        post_id.education_course_ids = post_id.blog_id.education_course_ids
        post_id.education_group_ids = post_id.blog_id.education_group_ids
        return post_id

    @api.multi
    def _compute_invited_partners(self):
        for record in self:
            record._onchange_post_info()

    @api.multi
    @api.onchange(
        'blog_id', 'blog_id.invited_partner_ids',
        'education_center_ids', 'education_course_ids', 'education_group_ids')
    def _onchange_post_info(self):
        domain = [
            ('id', 'in', self.blog_id.invited_partner_ids.ids)]
        if self.education_center_ids:
            domain += [
                ('current_center_id', 'in', self.education_center_ids.ids)]
        if self.education_course_ids:
            domain += [
                ('current_course_id', 'in', self.education_course_ids.ids)]
        if self.education_group_ids:
            domain += [
                ('current_group_id', 'in', self.education_group_ids.ids)]
        partners = self.env['res.partner'].search(domain)
        self.invited_partner_ids = partners.ids

    @api.multi
    def _compute_count_invited_partners(self):
        for record in self:
            record._onchange_count_invited_partners()

    @api.multi
    @api.onchange('invited_partner_ids')
    def _onchange_count_invited_partners(self):
        self.invited_count = len(self.invited_partner_ids)

    @api.multi
    def button_open_post_invitations(self):
        self.ensure_one()
        action = self.env.ref(
            'website_education_blog.action_post_open_invitations')
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [('id', 'in', self.invited_partner_ids.ids)],
            safe_eval(action.domain or '[]')])
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update({
            'search_default_partner_id': self.id,
            'default_partner_id': self.id,
        })
        action_dict.update({
            'domain': domain,
        })
        return action_dict

