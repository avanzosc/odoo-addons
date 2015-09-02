# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.one
    def _compute_manual_standard_cost(self):
        self.manual_standard_cost = (
            self.product_id.manual_standard_cost or
            self.product_template.manual_standard_cost)

    @api.one
    def _compute_childs_manual_standard_cost(self):
        self.childs_manual_standard_cost = 0
        for line in self.child_line_ids:
            self.childs_manual_standard_cost += (
                line.manual_standard_cost + line.childs_manual_standard_cost)

    manual_standard_cost = fields.Float(
        string='Manual Standard Cost', compute='_compute_manual_standard_cost',
        digits_compute=dp.get_precision('Product Price'))
    childs_manual_standard_cost = fields.Float(
        string='Childs Manual Standard Cost',
        compute='_compute_childs_manual_standard_cost',
        digits_compute=dp.get_precision('Product Price'))
