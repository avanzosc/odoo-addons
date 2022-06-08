
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class BlogBlog(models.Model):
    _inherit = "blog.blog"

    future_students = fields.Boolean(
        string="Allow future students")
    academic_year_ids = fields.Many2many(
        string="Academic Years",
        comodel_name="education.academic_year")
    invited_future_lead_ids = fields.Many2many(
        string="Invited Leads",
        comodel_name="crm.lead.future.student",
        compute="_compute_future_invited_leads")
    invited_future_count = fields.Integer(
        string="Count Invited People",)

    @api.depends("future_students", "education_course_ids")
    def _compute_future_invited_partners(self):
        future_student_obj = self.env["crm.lead.future.student"]
        for record in self:
            if record.future_students:
                domain = []
                if record.academic_year_ids:
                    domain += [('academic_year_id', "in", record.academic_year_ids.ids),]
                if record.education_center_ids:
                    domain += [("enrollment_center_id", "in", record.education_center_ids.ids),]
                if record.education_course_ids:
                    domain += [("enrollment_course_id", "in", record.education_course_ids.ids),]
                lead_students = future_student_obj.search(domain)
                record.invited_future_lead_ids = [(6, 0, lead_students.ids)]

    @api.depends("invited_future_lead_ids")
    def _compute_future_invited_partners(self):
        for record in self:
            if record.future_students and record.invited_future_lead_ids:
                record.invited_partner_ids = record.invited_future_lead_ids.mapped('child_id').ids

            record.invited_future_count = len(record.invited_future_lead_ids)

    @api.multi
    def button_open_blog_future_invitations(self):
        self.ensure_one()
        action = self.env.ref(
            "website_education_blog_crm.action_blog_open_future_invitations")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("id", "in", self.invited_future_lead_ids.ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({
            "domain": domain,
        })
        return action_dict
