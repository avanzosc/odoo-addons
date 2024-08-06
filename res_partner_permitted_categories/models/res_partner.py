from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    permitted_web_categories = fields.Many2many(
        "product.public.category",
        relation="partner_permitted_categories_rel",
        column1="partner_id",
        column2="category_id",
        help="Categories this partner is allowed to see on the website. \
        If no category is selected, this filter will not be activated.",
    )
