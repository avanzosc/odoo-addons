from odoo import api, fields, models


class WebsitePage(models.Model):
    _inherit = 'website.page'

    website_require_login = fields.Boolean(
        string='Require login for website page access',
        help='If set, a user must be logged in to be able to access '
             'website page.',
        default=False,
    )

    @api.one
    def _compute_visible(self):
        super(WebsitePage, self)._compute_visible()
        self.is_visible = self.is_visible and not self.website_require_login
