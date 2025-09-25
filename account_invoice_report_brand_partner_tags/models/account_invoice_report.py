from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    brand_id = fields.Many2one("product.brand", string="Product Brand", readonly=True)

    partner_category_ids = fields.Many2many(
        "res.partner.category",
        string="contact labels",
        store=False,
        readonly=True,
        search="_search_partner_category_ids",
    )

    def _select(self):
        select = super()._select()
        select += ", pt_brand.product_brand_id AS brand_id"
        return select

    def _from(self):
        from_ = super()._from()
        from_ += """
            LEFT JOIN product_product pp_brand
                   ON pp_brand.id = line.product_id
            LEFT JOIN product_template pt_brand
                   ON pt_brand.id = pp_brand.product_tmpl_id
        """
        return from_

    def _group_by(self):
        group_by = super()._group_by()
        group_by += ", pt_brand.product_brand_id"
        return group_by

    def _search_partner_category_ids(self, operator, value):
        return [("commercial_partner_id.category_id", operator, value)]
