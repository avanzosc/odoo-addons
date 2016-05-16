# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.multi
    def _compute_manual_standard_cost(self):
        for line in self:
            if line.product_id:
                line.manual_standard_cost =\
                    line.product_id.manual_standard_cost
            else:
                try:
                    line.manual_standard_cost =\
                        line.product_tmpl_id.manual_standard_cost
                except:
                    line.manual_standard_cost = 0.0

    @api.depends('child_line_ids')
    def _compute_childs_manual_standard_cost(self):
        for bom_line in self:
            childs_manual_standard_cost = 0.0
            for line in bom_line.child_line_ids:
                childs_manual_standard_cost += (
                    line.manual_standard_cost +
                    line.childs_manual_standard_cost)
            bom_line.childs_manual_standard_cost = childs_manual_standard_cost

    manual_standard_cost = fields.Float(
        string='Manual Standard Cost', compute='_compute_manual_standard_cost',
        digits_compute=dp.get_precision('Product Price'))
    childs_manual_standard_cost = fields.Float(
        string='Childs Manual Standard Cost',
        compute='_compute_childs_manual_standard_cost',
        digits_compute=dp.get_precision('Product Price'))
