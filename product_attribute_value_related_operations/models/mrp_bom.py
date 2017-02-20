# -*- coding: utf-8 -*-
# © 2017 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, models


class MrpBom(models.Model):

    _inherit = 'mrp.bom'

    def _get_values_operations(self, production):
        if production.product_id:
            return production.product_id.attribute_value_ids.mapped(
                'operation_ids')
        else:
            return production.product_attribute_ids.mapped(
                'value_id.operation_ids')

    @api.model
    def _skip_bom_line(self, line, product):
        delete_product_lines = self._get_values_operations(
            self._context.get('production'))
        if line.operation.operation in delete_product_lines:
            return True
        return super(MrpBom, self)._skip_bom_line(line, product)

    @api.multi
    def _prepare_wc_line(self, wc_use, level=0, factor=1):
        res = super(MrpBom, self)._prepare_wc_line(wc_use, level=level,
                                                   factor=factor)
        production = self._context.get('production')
        if production:
            operations_remove = \
                self._get_values_operations(production)
            if wc_use.operation in operations_remove:
                return {}
        return res

    def _bom_explode(self, product, factor, properties=None, level=0,
                     routing_id=False, previous_products=None,
                     master_bom=None):
        result, result2 = super(MrpBom, self)._bom_explode(
            product, factor, properties=properties, level=level,
            routing_id=routing_id, previous_products=previous_products,
            master_bom=master_bom)
        return result, filter(lambda x: x.get('workcenter_id'), result2)
