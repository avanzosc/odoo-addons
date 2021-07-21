from odoo import fields, models


class Slide(models.Model):
    _inherit = 'slide.slide'

    add_attachment = fields.Boolean("Ask for attachment")
