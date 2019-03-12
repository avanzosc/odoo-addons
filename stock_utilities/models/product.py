# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.multi
    def _compute_count_orderpoints(self):
        orderpoint_model = self.env['stock.warehouse.orderpoint']
        for record in self:
            cond = [('product_tmpl_id', '=', record.id)]
            products = self.env['product.product'].search(cond)
            domain = [('product_id', 'in', products.ids)]
            record.count_orderpoints = orderpoint_model.search_count(domain)

    count_orderpoints = fields.Float(string="Count Orderpoints",
                                     compute="_compute_count_orderpoints")


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.multi
    def _compute_count_orderpoints(self):
        orderpoint_model = self.env['stock.warehouse.orderpoint']
        for record in self:
            domain = [('product_id', '=', record.id)]
            record.count_orderpoints = orderpoint_model.search_count(domain)

    count_orderpoints = fields.Float(string="Count Orderpoints",
                                     compute="_compute_count_orderpoints")
