# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import logging

from odoo import api, models

from .ir_translation import debrand

_logger = logging.getLogger(__name__)

MODULE = "_web_debranding"


class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.model
    def create(self, values):
        subject = values.get("subject")
        channel_all_employees = self.env.ref(
            "mail.channel_all_employees", raise_if_not_found=False
        )
        if (
            channel_all_employees
            and subject
            and values.get("model") == "mail.channel"
            and channel_all_employees.id == values.get("res_id")
            and subject.endswith("application installed!")
        ):
            values["body"] = debrand(self.env, values.get("body", ""))
        return super(MailMessage, self).create(values)
