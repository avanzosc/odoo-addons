
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class BlogPost(models.Model):
    _inherit = "blog.post"

    future_students = fields.Boolean(
        related="blog_id.future_students")
    invited_future_lead_ids = fields.Many2many(
        string="Invited Leads",
        comodel_name="crm.lead.future.student",
        compute="_compute_future_invited_leads", store=True)
    invited_future_count = fields.Integer(
        string="Count Invited Future People",)

    @api.depends("allowed_group_ids")
    def _compute_invited_partners(self):
        for record in self:
            if not record.future_students:
                super(BlogPost, self)._compute_invited_partners()
            else:
                record._compute_future_invited_leads()

    @api.depends("future_students", "education_course_ids", "education_center_ids")
    def _compute_future_invited_leads(self):
        future_student_obj = self.env["crm.lead.future.student"]
        for record in self:
            if record.future_students:
                domain = [
                    ('id', 'in', record.blog_id.invited_future_lead_ids.ids)]
                if record.education_center_ids:
                    domain += [
                        ("school_id", "in", record.education_center_ids.ids),]
                if record.education_course_ids:
                    domain += [
                        ("course_id", "in", record.education_course_ids.ids),]
                lead_students = future_student_obj.search(domain)
                record.invited_future_lead_ids = [(6, 0, lead_students.ids)]
                record.invited_partner_ids = [
                    (6, 0, record.invited_future_lead_ids.mapped('child_id').ids)]
                record.invited_future_count = len(
                    record.invited_future_lead_ids)
                record.invited_count = len(record.invited_partner_ids)

    @api.multi
    def button_open_post_future_invitations(self):
        self.ensure_one()
        action = self.env.ref(
            "website_education_blog_crm.action_post_open_future_invitations")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("id", "in", self.invited_future_lead_ids.ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({
            "domain": domain,
        })
        return action_dict
