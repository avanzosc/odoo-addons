# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_line = fields.Many2one(store=True)

    @api.multi
    def _action_compute_lines(self, properties):
        res = super(MrpProduction, self.with_context(production=self)
                    )._action_compute_lines(properties=properties)
        sale_line = self.env.context.get('sale_line', False)
        if sale_line:
            self.mapped('product_lines').write({'sale_line_id': sale_line})
        return res

    @api.multi
    def write(self, values, update=True, mini=True):
        for record in self:
            super(MrpProduction, record).write(
                values, update=update, mini=mini)
            if 'product_qty' in values:
                record.sale_line.write({
                    'product_uom_qty': record.product_qty,
                    'price_unit': record.production_total / record.product_qty,
                })
        return True


class MrpProductionProductLine(models.Model):
    _inherit = 'mrp.production.product.line'

    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line', string='Sale lines', copy=False)
