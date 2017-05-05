# -*- coding: utf-8 -*-
from openerp import http
import openerp.addons.website_sale.controllers.main as main
from openerp.http import request
import logging
_log = logging.getLogger(__name__)


class WebsiteSale(main.website_sale):
    @http.route()
    def product(self, product, category='', search='', **kwargs):
        res = super(WebsiteSale, self).product(
            product=product, category=category, search=search, **kwargs)
        env = request.env
        invoices = None
        products = []
        if request.uid != request.website.user_id.id:
            invoices = env['account.invoice'].sudo().search([
                ('partner_id', '=', env.user.partner_id.id),
                ('state', 'in', ['open', 'paid'])])
            if invoices:
                for i in invoices:
                    for l in i.invoice_line:
                        products.append(l.product_id.id)
        res.qcontext['purchased'] = product.id in products
        res.qcontext['subscribed'] = False
        return res


class WebsiteProductTrainingPlan(main.website_sale):
    @http.route(
        ['/shop/product/<model("product.template"):product>/training-plan/'
         '<model("product.training.plan"):training>/'],
        type='http', auth="public", website=True)
    def product_plan_list(self, training, product):
        return http.request.render('website_product_training_plan.training', {
            'training': training,
            'product': product
        })

    @http.route(
        ['/training-plan'],
        type='http', auth="public", website=True)
    def list(self):
        env = request.env
        trainings = env['product.training.plan'].search([])
        return http.request.render(
            'website_product_training_plan.all_training_plan_list', {
                'trainings': trainings})
