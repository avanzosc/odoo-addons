# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from datetime import datetime

from odoo import _, fields, models


class ProductPricelistItem(models.Model):
    _name = "product.pricelist.item"
    _inherit = [
        "product.pricelist.item",
        "portal.mixin",
        "mail.thread",
        "mail.activity.mixin",
    ]

    product_default_code = fields.Char(
        string="Product default code", related="product_tmpl_id.default_code"
    )
    applied_on = fields.Selection(tracking=True)
    min_quantity = fields.Integer(tracking=True)
    compute_price = fields.Selection(tracking=True)
    fixed_price = fields.Float(tracking=True)
    percent_price = fields.Float(tracking=True)

    def unlink(self):
        for item in self:
            message = _("Has been deleted the price list : %(price_list_name)s") % {
                "price_list_name": item.name
            }
            if item.applied_on == "3_global":
                message = _("%(message)s, applied on Global") % {"message": message}
            if item.applied_on == "2_product_category":
                message = _(
                    "%(message)s, applied on product category %(category_name)s"
                ) % {"message": message, "category_name": item.categ_id.name}
            if item.applied_on == "1_product":
                message = _("%(message)s, applied on product %(product_name)s") % {
                    "message": message,
                    "product_name": item.product_tmpl_id.name,
                }
            if item.applied_on == "1_product":
                message = _(
                    "%(message)s, applied on product variant %(product_variant_name)s"
                ) % {"message": message, "product_variant_name": item.product_id.name}
            if item.compute_price == "fixed":
                message = _(
                    "%(message)s, price calculation mode: Fixed, price: %(fixed_price)s"
                ) % {"message": message, "fixed_price": item.fixed_price}
            if item.compute_price == "percentage":
                message = _(
                    "%(message)s, price calculation mode: Percentage, percentage: %(percent_price)s%%"
                ) % {"message": message, "percent_price": item.percent_price}
            message = _("%(message)s, min. quantity: %(min_quantity)s") % {
                "message": message,
                "min_quantity": item.min_quantity,
            }
            if item.date_start:
                message = _("%(message)s, date start: %(date_start)s") % {
                    "message": message,
                    "date_start": datetime.strftime(item.date_start, "%d-%m-%Y"),
                }
            if item.date_end:
                message = _("%(message)s, date end: %(date_end)s") % {
                    "message": message,
                    "date_end": datetime.strftime(item.date_end, "%d-%m-%Y"),
                }
            vals = {
                "type": "notification",
                "model": item.pricelist_id._name,
                "record_name": item.pricelist_id.name,
                "res_id": item.pricelist_id.id,
                "body": message,
            }
            self.env["mail.message"].create(vals)
        return super().unlink()
