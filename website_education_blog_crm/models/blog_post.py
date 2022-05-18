
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class BlogPost(models.Model):
    _inherit = "blog.post"

    future_students = fields.Boolean(
        related="blog_id.future_students")
    invited_future_lead_ids = fields.Many2many(
        related="blog_id.invited_future_lead_ids")
    invited_future_partner_ids = fields.Many2many(
        related="blog_id.invited_future_partner_ids")
    invited_future_count = fields.Integer(
        related="blog_id.invited_future_count")

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
