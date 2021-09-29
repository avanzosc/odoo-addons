
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
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year",
        string="Academic Year")
    education_center_ids = fields.Many2many(
        string="Education Centers",
        comodel_name="res.partner",
        relation="post_center_rel",
        column1="post_id",
        column2="center_id")
    education_course_ids = fields.Many2many(
        string="Education Courses", comodel_name="education.course")
    education_group_ids = fields.Many2many(
        string="Education Groups", comodel_name="education.group")
    education_category_ids = fields.Char(
        string="Educational Category")

    invited_partner_ids = fields.Many2many(
        string="Invited Partners",
        comodel_name="res.partner",
        compute="_compute_invited_partners",
        store=True)
    invited_count = fields.Integer(
        string="Count Invited People",
        compute="_compute_invited_partners",
        store=True)

    allowed_group_ids = fields.Many2many(
        string="Allowed Groups",
        comodel_name="education.group",
        compute="_compute_allowed_group_ids",
        relation="blog_post_group_rel",
        column1="post_id",
        column2="group_id",
        store=True)

    @api.depends("blog_id", "blog_id.allowed_group_ids", "academic_year_id",
                 "education_center_ids", "education_course_ids",
                 "education_group_ids")
    def _compute_allowed_group_ids(self):
        group_obj = self.env["education.group"]
        for record in self:
            groups = record.education_group_ids
            if not record.education_group_ids:
                domain = [("id", "in", record.blog_id.allowed_group_ids.ids)]
                if record.education_center_ids:
                    domain = expression.AND([
                        domain, [("center_id", "in",
                                  record.education_center_ids.ids)]])
                if record.education_course_ids:
                    domain = expression.AND([
                        domain, [("course_id", "in",
                                  record.education_course_ids.ids)]])
                groups = group_obj.search(domain)
            if record.academic_year_id:
                groups = groups.filtered(
                    lambda g: g.academic_year_id == record.academic_year_id)
            record.allowed_group_ids = [(6, 0, groups.ids)]

    @api.multi
    def _recompute_allowed_groups(self):
        for record in self:
            fields_list = ["allowed_group_ids"]
            for field in fields_list:
                self.env.add_todo(record._fields[field], record)
            record.recompute()

    @api.depends("allowed_group_ids")
    def _compute_invited_partners(self):
        partner_obj = self.env["res.partner"]
        for record in self:
            domain = [
                "|", ("student_group_ids", "in", record.allowed_group_ids.ids),
                ("progenitor_child_ids.student_group_ids", "in",
                 record.allowed_group_ids.ids),
            ]
            partners = partner_obj.search(domain)
            record.invited_partner_ids = [(6, 0, partners.ids)]
            record.invited_count = len(partners)

    @api.multi
    def button_open_post_invitations(self):
        self.ensure_one()
        action = self.env.ref(
            "website_education_blog.action_post_open_invitations")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("id", "in", self.invited_partner_ids.ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({
            "domain": domain,
        })
        return action_dict

