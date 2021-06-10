# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.http import request
from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventController(WebsiteEventController):

    def _create_attendees_from_registration_post(
            self, event, registration_data):
        res = super(WebsiteEventController, self
                    )._create_attendees_from_registration_post(
            event, registration_data)
        for registration in res:
            name = registration.name
            mail_name = name.replace(" ", ".")

            company_id = request.env.user.company_id
            user_default_domain = (
                company_id.portal_user_default_domain if company_id else '')

            registration.email = '%s@%s' % (mail_name.lower(),
                                            user_default_domain)

        return res
