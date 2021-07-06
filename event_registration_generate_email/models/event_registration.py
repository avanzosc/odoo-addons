
from odoo import models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def generate_user_email(self):
        name = self.name
        mail_name = name.replace(" ", ".")

        company_id = self.env.user.company_id
        user_default_domain = (
            company_id.portal_user_default_domain if company_id else '')

        result_email = '%s@%s' % (mail_name.lower(), user_default_domain)
        return result_email
