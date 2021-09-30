# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SlideSlidePartner(models.Model):
    _inherit = 'slide.slide.partner'

    def name_get(self):
        result = []
        for slide_slide_partner in self:
            display_name = u'{}: {}'.format(
                slide_slide_partner.channel_id.name,
                slide_slide_partner.slide_id.name)
            result.append((slide_slide_partner.id, display_name))
        return result
