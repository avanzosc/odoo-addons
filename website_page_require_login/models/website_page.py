from odoo import fields, models


class WebsitePage(models.Model):
    _inherit = 'website.page'

    website_require_login = fields.Boolean(
        string='Require login for website page access',
        help='If set, a user must be logged in to be able to access '
             'website page.',
        default=False,
    )
    