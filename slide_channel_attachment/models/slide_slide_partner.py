from odoo import fields, models


class SlidePartnerRelation(models.Model):
    _name = 'slide.slide.partner'
    _inherit = ['slide.slide.partner', "portal.mixin", "mail.thread",
                "mail.activity.mixin"]

    add_attachment = fields.Boolean("Ask for attachment",
                                    related="slide_id.add_attachment")
    slide_attachment = fields.Binary(string='Partner slide attachment')
    slide_attachment_name = fields.Char(string='Partner slide attachment name')
