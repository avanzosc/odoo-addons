from odoo import api, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def generate_user_email(self):
        company_id = self.env.user.company_id
        name = self.name
        result_email = name
        if company_id and name:
            mail_name = name.replace(" ", "_")
            result_email = mail_name.lower()
            user_default_domain = (
                company_id.portal_user_default_domain if company_id else ""
            )
            if user_default_domain:
                result_email = result_email + "@" + user_default_domain
        return result_email

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if "email" not in vals and "name" in vals:
            res.email = res.generate_user_email()
        return res
