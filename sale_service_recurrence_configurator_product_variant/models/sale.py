# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _sale_line_with_sale_quote_information(self, template, line):
        line = super(SaleOrder, self)._sale_line_with_sale_quote_information(
            template, line)
        line[2].update({
            'product_tmpl_id': template.product_template.id})
        return line
