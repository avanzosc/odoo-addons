# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _is_service_project(self):
        route_project = (
            self.env.ref('procurement_service_project.route_serv_project'))
        for product in self:
            if (product.type == 'service' and
                len(product.route_ids) == 1 and route_project.id in
                    product.route_ids.ids):
                return True
        return False

    @api.multi
    def need_procurement(self):
        for product in self:
            if product._is_service_project():
                return True
        return super(ProductProduct, self).need_procurement()
