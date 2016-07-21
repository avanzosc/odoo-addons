# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    volume_formula = fields.Text(string='Volume formula')
    weight_formula = fields.Text(string='Weight formula')
    weight_net_formula = fields.Text(string='Net weight formula')
    uos_coeff_formula = fields.Text(string='UOS coefficient formula')
    uop_coeff_formula = fields.Text(string='UOP coefficient formula')


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    calculated_volume = fields.Float(string="Volume",
                                     compute='_compute_dimensions')
    calculated_weight = fields.Float(string="Gross Weight",
                                     compute='_compute_dimensions')
    calculated_weight_net = fields.Float(string="Net Weight",
                                         compute='_compute_dimensions')
    uos_coeff = fields.Float(
        string='Unit of Measure -> UOS Coeff',
        digits= dp.get_precision('Product UoS'),
        help='Coefficient to convert default Unit '
             'of Measure to Unit of Sale\n uos = uom * coeff',
        compute='_compute_dimensions'
    )
    custom_uos_coeff = fields.Text(
        string='UOS coefficient formula',
        help='It must be written in reverse polish notation, '
             'example:\n example_attribute 2 *',
    )
    custom_uos_coeff_check = fields.Boolean(string='Custom coefficient')
    uop_coeff = fields.Float(
        string='Purchase Unit of Measure -> 2UoP Coeff',
        digits=dp.get_precision('Product UoP'),
        help='Coefficient to convert default Purchase Unit of Measure to'
        ' Secondary Unit of Purchase\n uop = uom * coeff',
        compute='_compute_dimensions')
    custom_uop_coeff = fields.Text(
        string='UOP coefficient formula',
        help='It must be written in reverse polish notation, '
             'example:\n example_attribute 2 *',
    )
    custom_uop_coeff_check = fields.Boolean(string='Custom coefficient')
    uop_coeff = fields.Float(
        string='Purchase Unit of Measure -> 2UoP Coeff',
        digits=dp.get_precision('Product UoP'),
        help='Coefficient to convert default Purchase Unit of Measure to'
        ' Secondary Unit of Purchase\n uop = uom * coeff',
        compute='_compute_dimensions')

    @api.onchange('custom_uos_coeff_check', 'custom_uos_coeff')
    def compute_uos_coeff(self):
        if not self.custom_uos_coeff_check:
            self.uos_coeff = self.calculate_expression(
                self.product_tmpl_id.uos_coeff_formula)
        else:
            self.uos_coeff = self.calculate_expression(
                self.custom_uos_coeff)

    @api.onchange('custom_uop_coeff_check', 'custom_uop_coeff')
    def compute_uop_coeff(self):
        if not self.custom_uop_coeff_check:
            self.uop_coeff = self.calculate_expression(
                self.product_tmpl_id.uop_coeff_formula)
        else:
            self.uop_coeff = self.calculate_expression(
                self.custom_uop_coeff)

    @api.depends('product_tmpl_id.volume_formula',
                 'product_tmpl_id.weight_formula',
                 'product_tmpl_id.weight_net_formula',
                 'product_tmpl_id.uos_coeff',
                 'product_tmpl_id.uop_coeff',
                 'custom_uos_coeff',
                 'custom_uop_coeff',
                 'attribute_value_ids')
    def _compute_dimensions(self):
        for product in self:
            tmpl = product.product_tmpl_id
            product.calculated_volume = product.calculate_expression(
                tmpl.volume_formula)
            product.calculated_weight = product.calculate_expression(
                tmpl.weight_formula)
            product.calculated_weight_net = product.calculate_expression(
                tmpl.weight_net_formula)
            if product.custom_uos_coeff_check:
                product.uos_coeff = product.calculate_expression(
                    product.custom_uos_coeff)
            else:
                product.uos_coeff = product.calculate_expression(
                    tmpl.uos_coeff_formula)
            if product.custom_uop_coeff_check:
                product.uop_coeff = product.calculate_expression(
                    product.custom_uop_coeff)
            else:
                product.uop_coeff = product.calculate_expression(
                    tmpl.uop_coeff_formula)

    def _normalize_formula(self, formula):
        return formula.strip().split(' ')

    def calculate_expression(self, formula):
        if formula:
            normalized_formula = self._normalize_formula(formula)
            return self.eval_expression(normalized_formula)

    def _get_val(self, val):
        try:
           return float(val)
        except ValueError:
            field = val.split('.')
            res = False
            if field and field[0] in ['self_t', 'self_p']:
                if field[0] == 'self_p':
                    res = float(self[field[1]])
                else:
                    res = float(self.product_tmpl_id[field[1]])
            elif field:
                res = self.attribute_value_ids.filtered(
                    lambda x: x.attribute_id.attribute_code == field[0]
                                                              ).numeric_value
        return res

    def eval_expression(self, formula):
        operators = ['-', '+', '*', '/']
        stack = []
        for val in formula:
            if val in operators:
                op1 = stack.pop()
                op2 = stack.pop()
                result = eval('{} {} {}'.format(op2, val, op1))
                stack.append(result)
            else:
                stack.append(self._get_val(val))
        return stack.pop()