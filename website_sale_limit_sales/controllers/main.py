
from odoo.http import request
from datetime import date, timedelta
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class WebsiteSale(WebsiteSale):

    def _get_limited_brands(self, order):
        order_lines = order.order_line
        limited_brand_list = None
        limited_order_lines = order_lines.filtered(
            lambda l: l.product_id.product_brand_id.max_per_order > 0 or
                      l.product_id.product_brand_id.max_per_product_order > 0
        )

        if limited_order_lines:
            limited_brand_list = limited_order_lines.mapped(
                'product_id.product_brand_id')

        return limited_brand_list

    def _compute_disable_shopping(self, user_id, order):
        order_lines = order.order_line
        # GET ALL LIMITED BRANDS
        limited_brand_list = self._get_limited_brands(order)
        disable_message = None
        if limited_brand_list:
            for brand in limited_brand_list:
                max_brand_qty = brand.max_per_order
                max_brand_qty_per_product = brand.max_per_product_order
                # Cuántas uds de la marca tiene?
                brand_order_lines = order_lines.filtered(
                    lambda l: l.product_id.product_brand_id.id == brand.id)
                if brand_order_lines:
                    disable_message = self._limit_brand_sales_per_days(brand)
                    if disable_message:
                        return disable_message

                brand_qty = 0
                limited_categories = brand.limited_categories
                limit_true = False
                for line in brand_order_lines:
                    if not limited_categories or line.product_id.categ_id \
                            in limited_categories:
                        if line.product_uom_qty > max_brand_qty_per_product:
                            limit_true = True
                        brand_qty += line.product_uom_qty

                if brand_qty > max_brand_qty or limit_true:
                    disable_message = self._get_brand_info_message(brand)
        return disable_message

    def _get_last_confirmed_order(self, user_id):
        last_confirmed_order = request.env['sale.order'].search(
            [('partner_id', '=', user_id.partner_id.id),
             ('state', '=', 'done')],
            order='confirmation_date desc',
            limit=1
        )
        return last_confirmed_order

    def _limit_brand_sales_per_days(self, brand):
        user_id = request.env['res.users'].browse(request.uid)
        last_confirmed_order = self._get_last_confirmed_order(user_id)
        if brand.limit_expiration_days > 0 and last_confirmed_order and\
                last_confirmed_order.confirmation_date:
            brand_order_lines = \
                last_confirmed_order.order_line.sudo().filtered(
                    lambda l: l.product_id.product_brand_id.id == brand.id)
            if brand_order_lines:
                c_date = last_confirmed_order.confirmation_date
                # Ha hecho alguna compra de esta marca en el límite permitido?
                limit_date = c_date + timedelta(
                    days=brand.limit_expiration_days)
                if date.today().strftime(DEFAULT_SERVER_DATE_FORMAT) <= \
                        limit_date.strftime(DEFAULT_SERVER_DATE_FORMAT):
                    disable_message = self._get_brand_info_message(brand)
                    return disable_message
        return None

    def _limit_sales_per_day(self):
        user_id = request.env['res.users'].browse(request.uid)
        last_confirmed_order = self._get_last_confirmed_order(user_id)
        if last_confirmed_order and last_confirmed_order.confirmation_date:
            c_date = last_confirmed_order.confirmation_date
            # Ha hecho alguna compra hoy?
            if c_date.strftime(DEFAULT_SERVER_DATE_FORMAT) == \
                    date.today().strftime(DEFAULT_SERVER_DATE_FORMAT):
                disable_message = 'YOU ALREADY DID A PURCHASE TODAY!'
                return disable_message
        return None

    def _get_limitation_info_message(self):
        info_message = None
        limited_brands = request.env['product.brand'].sudo().search(
            [('max_per_order', '>', 0),
             ('max_per_product_order', '>', 0)])
        for brand in limited_brands:
            if brand.limit_expiration_days:
                info_message = self._get_brand_info_message(brand)
        return info_message

    def _get_brand_info_message(self, brand):
        disable_message = "THE MOST %s" % brand.name
        if brand.limited_categories:
            limited_categories_list = " ".join(brand.limited_categories.mapped(
                'display_name'))
            disable_message += " %s" % (limited_categories_list)
        disable_message += " YOU CAN ORDER"
        if brand.limit_expiration_days:
            disable_message += " IN %d DAYS" % (brand.limit_expiration_days)
        disable_message += " IS %d UNITS PER MODEL AND %d IN TOTAL" % (
            brand.max_per_product_order, brand.max_per_order)
        return disable_message
