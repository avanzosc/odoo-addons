
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, tools, _
from odoo.http import request
from datetime import date, datetime, timedelta
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class WebsiteSale(WebsiteSale):

    def _compute_disable_shopping(self, user_id, order):
        order_lines = order.order_line
        # GET ALL LIMITED BRANDS
        limited_brand_list = None
        limited_order_lines = order_lines.filtered(
                        lambda l: l.product_id.product_brand_id.max_per_order > 0 or
                        l.product_id.product_brand_id.max_per_product_order > 0
        )

        if limited_order_lines:
            limited_brand_list = limited_order_lines.mapped('product_id.product_brand_id')

        disable_message = None
        for brand in limited_brand_list:
            max_brand_qty = brand.max_per_order
            max_brand_qty_per_product = brand.max_per_product_order

            # Cuántas uds de la marca tiene?
            brand_order_lines = order_lines.filtered(lambda l: l.product_id.product_brand_id.id == brand.id)
            brand_qty = 0
            limited_categories = brand.limited_categories
            for line in brand_order_lines:
                if not limited_categories or line.product_id.categ_id in limited_categories:
                    if line.product_uom_qty > max_brand_qty_per_product:
                        if limited_categories:
                            limited_categories_list = " ".join(limited_categories.mapped('display_name'))
                            disable_message = 'YOU CAN ONLY ADD %d UNITS FROM EACH PRODUCT OF THE CATEGORY(es) %s OF THE BRAND %s!' % \
                                          (max_brand_qty_per_product, limited_categories_list, brand.name)
                        else:
                            disable_message = 'YOU CAN ONLY ADD %d UNITS FROM EACH PRODUCT OF THE BRAND %s!' % \
                                          (max_brand_qty_per_product, brand.name)
                        return disable_message
                    brand_qty += line.product_uom_qty

            if brand_qty > max_brand_qty:
                if limited_categories:
                    limited_categories_list = " ".join(limited_categories.mapped('display_name'))
                    disable_message = 'YOU CAN ONLY ADD %d UNITS FROM THE CATEGORY(es) %s OF THE BRAND %s!' % \
                                      (max_brand_qty, limited_categories_list, brand.name)
                else:
                    disable_message = 'YOU CAN ONLY ADD %d UNITS FROM THE BRAND %s!' % (max_brand_qty, brand.name)

        return disable_message

    def _get_last_confirmed_order(self, user_id):
        last_confirmed_order = request.env['sale.order'].search(
            [('partner_id', '=', user_id.partner_id.id),
             ('state', '=', 'done')],
            order='confirmation_date desc',
            limit=1
        )
        return last_confirmed_order

    def _limit_sales_per_day(self):
        user_id = request.env['res.users'].browse(request.uid)
        last_confirmed_order = self._get_last_confirmed_order(user_id)
        if last_confirmed_order and last_confirmed_order.confirmation_date:
            c_date = last_confirmed_order.confirmation_date
            # Ha hecho alguna compra hoy?
            if c_date.strftime(DEFAULT_SERVER_DATE_FORMAT) == date.today().strftime(DEFAULT_SERVER_DATE_FORMAT):
                disable_message = 'YOU ALREADY DID A PURCHASE TODAY!'
                return disable_message
        return None
