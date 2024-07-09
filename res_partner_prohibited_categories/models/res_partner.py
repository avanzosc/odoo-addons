from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    prohibited_category_ids = fields.Many2many(
        "product.public.category",
        string="Prohibited Product Categories",
        help="These are the product categories that are prohibited for this partner.",
    )

    related_prohibited_category_ids = fields.Many2many(
        comodel_name="product.public.category",
        relation="partner_pick_up_point_prohibited_rel",
        column1="partner_id",
        column2="category_id",
        compute="_compute_related_prohibited_category_ids",
        string="Related Prohibited Product Categories",
        help="Prohibited product categories from the pick up point.",
    )

    @api.depends("pick_up_point_id.prohibited_category_ids")
    def _compute_related_prohibited_category_ids(self):
        for partner in self:
            partner.related_prohibited_category_ids = (
                partner.pick_up_point_id.prohibited_category_ids
            )
