# -*- coding: utf-8 -*-
from openerp import http
import openerp.addons.website_sale.controllers.main as main
from openerp.http import request


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
        cr, uid, context, pool = request.cr, request.uid, request.context, \
                                 request.registry
        training_obj = pool['product.training.plan']
        training_ids = training_obj.search(cr, uid, [], context=context)
        return http.request.render(
            'website_product_training_plan.all_training_plan_list',
            {'trainings': training_obj.browse(cr, uid, training_ids,
                                              context=context),
            })
