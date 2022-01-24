
from odoo import api, fields, models


class SlideSlide(models.Model):
    _inherit = 'slide.slide'

    by_tutor = fields.Boolean('Complete by Tutor')

    @api.onchange('by_tutor', 'is_published')
    def _onchange_by_tutor(self):
        for record in self:
            if record.by_tutor:
                record.is_published = False
