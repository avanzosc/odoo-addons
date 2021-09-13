
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class BlogBlog(models.Model):
    _inherit = "blog.blog"

    education_center_ids = fields.Many2many(
        string='Education Centers',
        comodel_name="res.partner",
        relation='blog_center_rel',
        column1='blog_id',
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

    @api.multi
    def _compute_invited_partners(self):
        for record in self:
            record._onchange_blog_info()

    @api.multi
    @api.onchange(
        'education_center_ids', 'education_course_ids', 'education_group_ids')
    def _onchange_blog_info(self):
        domain = [
            ('educational_category', 'not in', ('school', 'federation'))]
        if self.education_center_ids:
            domain += [
                '|',
                ('current_center_id', 'in', self.education_center_ids.ids),
                ('progenitor_child_ids.current_center_id', 'in', self.education_center_ids.ids)]
        if self.education_course_ids:
            domain += [
                '|',
                ('current_course_id', 'in', self.education_course_ids.ids),
                ('progenitor_child_ids.current_course_id', 'in', self.education_center_ids.ids)]
        if self.education_group_ids:
            domain += [
                '|',
                ('current_group_id', 'in', self.education_group_ids.ids),
                ('progenitor_child_ids.current_group_id', 'in', self.education_center_ids.ids)]
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
    def button_open_blog_invitations(self):
        self.ensure_one()
        action = self.env.ref(
            'website_education_blog.action_blog_open_invitations')
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
