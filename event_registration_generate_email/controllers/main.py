# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventController(WebsiteEventController):

    def _create_attendees_from_registration_post(
            self, event, registration_data):
        res = super(WebsiteEventController, self
                    )._create_attendees_from_registration_post(
            event, registration_data)
        for registration in res:
            registration.email = registration.generate_user_email()
        return res
