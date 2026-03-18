from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    owner_partner_ids = fields.Many2many(
        "res.partner",
        string="Client Owners",
        help="Select up to 3 owners for this product.",
        domain="[('is_company', '=', True)]",
    )

    @api.constrains("owner_partner_ids")
    def _check_owner_partner_ids(self):
        for record in self:
            if len(record.owner_partner_ids) > 3:
                raise models.ValidationError(
                    _("You can only assign up to 3 owners to a product.")
                )
