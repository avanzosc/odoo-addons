# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError
from openerp.models import expression
from openerp.addons import decimal_precision as dp
import logging
import re

_logger = logging.getLogger(__name__)

class MrpBom(models.Model):

    _inherit = 'mrp.bom'



    @api.model
    def _factor(self, factor, product_efficiency, product_rounding,
                bom_line=None):
        if not bom_line:
            return super(MrpBom, self)._factor(
                factor, product_efficiency, product_rounding)
        formula_qty = bom_line.line_qty()
        return super(MrpBom, self)._factor(
            factor*formula_qty, product_efficiency, product_rounding)

    def _set_replace_attribute_values(self, attrs, calculated_attrs):
        calc_attrs = calculated_attrs.keys()
        attr_obj = self.env['product.attribute']
        for val in attrs:
            val = val[2]
            attribute_id = val['attribute_id']
            if attribute_id in calc_attrs:
                custom_value = calculated_attrs[attribute_id][1] if \
                    attr_obj.browse(attribute_id).attr_type == 'range' else \
                    False
                val.update({'value_id': calculated_attrs[attribute_id][0],
                            'custom_value': custom_value})

    def _get_attribute_value(self, eval_value, attribute_id):
        value_obj = self.env['product.attribute.value']
        custom_value = False
        value_id = False
        if isinstance(eval_value, (int, float)):
            value = round(eval_value, self.env.ref(
                'bom_lines_configurator.precision_in_formula').digits)
            if attribute_id.attr_type == 'select':
                value_id = value_obj.search([(
                    'attribute_id', '=', attribute_id.id),
                    ('name', '=', str(int(value)))
                ])
            elif attribute_id.attr_type == 'numeric':
                value_id = value_obj.search([(
                    'attribute_id', '=', attribute_id.id),
                    ('numeric_value', '=', value)
                ])
            elif attribute_id.attr_type == 'range':
                value_id = value_obj.search([(
                    'attribute_id', '=', attribute_id.id),
                    ('min_range', '<=', value), ('max_range', '>=', value)
                ])[:1]
                #_logger.info(u"Range attribute values: value - {}, attribute "
                #             u"- {} attribute-id - {} all_values - {}"
                #             u"".format(value, attribute_id.name,
                # attribute_id.id, value_obj.search([('attribute_id', '=', attribute_id.id)])))
                custom_value = value
        else:
            value_id = eval_value
        #_logger.info(u"value_id : {}, for attribute: {}. custom_value"
        #             u": {}".format(value_id and value_id.name, \
        #                            attribute_id.name, custom_value))
        return value_id, custom_value

    def _all_attributes_has_value(self, values):
        tmpl_id = self.env['product.template'].browse(values.get(
            'product_tmpl_id'))
        tmpl_attrs = tmpl_id.attribute_line_ids.mapped('attribute_id.id')
        attrs = values.get('product_attribute_ids')
        attr_ids = map(lambda x: x[2].get('attribute_id') if x[2].get(
            'value_id') else False, attrs)
        return set(tmpl_attrs) == set(attr_ids)

    @api.model
    def _prepare_consume_line(self, bom_line, quantity, factor=1):
        res = super(MrpBom, self)._prepare_consume_line(bom_line, quantity,
                                                        factor=factor)
        # if not quantity:
        #     return
        #if not res.get('product_id'):
        tmpl_id = bom_line.product_tmpl_id
        calculated_attrs = {}
        acts = bom_line._prepare_acts()
        for line in bom_line.attribute_selections_ids:
            if line.eval_rule(acts):
                #_logger.info("Product attributes: {} - {}".format(
                #    res['name'], line.attribute_id.name))
                eval_value = line.eval_formula(acts)
                value_id, custom_value = self._get_attribute_value(
                    eval_value, line.attribute_id)
                if value_id and not calculated_attrs.get(line.attribute_id.id):
                    calculated_attrs[line.attribute_id.id] = (value_id.id,
                                                              custom_value)
        self._set_replace_attribute_values(res['product_attribute_ids'],
                                           calculated_attrs)
        comp_product = self.env['product.product']._product_find(
            tmpl_id, map(lambda x: x[2], res['product_attribute_ids']))
        comp_product = comp_product and comp_product.id
        if not comp_product and self._all_attributes_has_value(res):
            comp_product = self.env[
                'product.configurator']._create_variant_from_vals(
                res).get('product_id')
        res['product_id'] = comp_product
        #_logger.info("product to consume: {}".format(unicode(res)))
        return res

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    attribute_rule_ids = fields.One2many(comodel_name='mrp.bom.line.rule',
                                         inverse_name='bom_line_id',
                                         string='Rule lines')
    attribute_selections_ids = fields.One2many(
        comodel_name='mrp.bom.line.variant.selector',
        inverse_name='bom_line_id',
        string='Attribute value selection'
    )
    possible_attribute_ids = fields.Many2many(
         comodel_name='product.attribute', compute="_compute_attribute_ids")

    @api.model
    def _compute_attribute_ids(self):
        self.possible_attribute_ids = self.product_tmpl_id.mapped(
             'attribute_line_ids.attribute_id')

    @api.multi
    def button_save_data(self):
        return True

    @api.multi
    def button_details(self):
        context = self.env.context.copy()
        context['view_buttons'] = True
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.bom.line',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'readonly': True,
            'res_id': self.id,
            'context': context
        }
        return view

    def _prepare_acts(self):
        production = self.env.context.get('production')
        return production.product_attribute_ids

    def _check_rules(self, acts):
        if not self.attribute_rule_ids:
            return 1
        for rule_line in self.attribute_rule_ids:
            if rule_line.eval_rule(acts):
                return rule_line.eval_formula(acts)
        return 0

    def line_qty(self):
        acts = self._prepare_acts()
        return self._check_rules(acts)

    @api.multi
    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        res = super(MrpBomLine, self).onchange_product_tmpl_id()
        if self.product_tmpl_id:
            self.attribute_rule_ids = self.attribute_rule_ids.mapped(
                lambda x: (2, x.id))
            return {'domain': {'product_id': [('product_tmpl_id', '=',
                                               self.product_tmpl_id.id)]}}
        return res


class MrpBomLineRule(models.Model):
    _name = 'mrp.bom.line.rule'
    _rec_name = 'sequence'

    sequence = fields.Integer(default=1)
    formula_qty = fields.Char(string='Formula')
    conditions = fields.Text(string='Conditions')
    bom_line_id = fields.Many2one(comodel_name='mrp.bom.line', string='Bom '
                                                                      'line')

    def get_formula(self):
        return self.formula_qty.strip().split(' ')

    def convert_operator(self, ope):
        if ope == '=':
            return '=='
        elif ope in ['!=', '<=', '>=', '<', '>', 'in', 'not in']:
            return ope

    def calculate_leaf(self, arg, attr_values):
        attr_name, ope, value = arg
        operator = self.convert_operator(ope)
        attr = self.env['product.attribute'].search([('attribute_code', '=',
                                                      attr_name)])
        product_attr_value = filter(
            lambda x: x.attribute_id == attr, attr_values)
        if product_attr_value:
            attr_value = product_attr_value[0]
            if attr_value.attribute_id.attr_type == 'select':
                return eval(u"{} {} {}".format(
                    u"unicode(attr_value.value_id.attribute_code)", operator,
                    u"value"))
            elif attr_value.attribute_id.attr_type == 'numeric':
                if isinstance(value, list):
                    return eval("{} {} {}".format(
                        "attr_value.value_id.numeric_value", operator,
                        "map(lambda x: float(x), value)"))
                else:
                    return eval("{} {} {}".format(
                        "attr_value.value_id.numeric_value", operator,
                        "float(value)"))
            elif attr_value.attribute_id.attr_type == 'range':
                if isinstance(value, list):
                    return eval("{} {} {}".format(
                        "attr_value.custom_value", operator,
                        "map(lambda x: float(x), value)"))
                else:
                    return eval("{} {} {}".format(
                        "attr_value.custom_value", operator,
                        "float(value)"))
            else:
                return True
        return

    def eval_rule(self, acts):
        return self.eval_expression(expression.normalize_domain(eval(
            self.conditions)), acts)

    def eval_expression(self, arg, attr_values):
        element = arg[0]
        del arg[0]
        if isinstance(element, bool):
            return element
        if expression.is_leaf(element):
            return self.calculate_leaf(element, attr_values)
        if expression.is_operator(element):
            if element == '|':
                cond = self.eval_expression(arg, attr_values)
                return self.eval_expression(arg, attr_values) or cond
            elif element == '&':
                cond = self.eval_expression(arg, attr_values)
                return self.eval_expression(arg, attr_values) and cond
            elif element == '!':
                return not self.eval_expression(arg, attr_values)

    def eval_formula(self, established_values):
        operators = ['-', '+', '*', '/', '**', '//']
        stack = []
        for val in self.get_formula():
            if val in operators:
                op1 = stack.pop()
                op2 = stack.pop()
                try:
                    result = eval('{} {} {}'.format(op2, val, op1))
                except:
                    raise UserError(
                        _(u'Error evaluating formula: {}\non product: {}, '
                          u'condition: {}'.format(self.formula_qty,
                            self.bom_line_id.product_tmpl_id.name,
                            self.conditions)))
                stack.append(result)
            else:
                value = self._get_val(val, established_values)
                #_logger.info(u"get value of: {}, from formula: {}. returned "
                #             u"value: {}".format(val, self.get_formula(),
                #                                 value))
                stack.append(value)
        return stack.pop()

    def _get_val(self, field, values):
        field_value = field.split('.')
        if len(field_value) == 2 and field_value[0] in ['const', 'parent']:
            if field_value[0] == 'const':
                return self.env['mrp.constant'].search(
                    [('name', '=', field_value[1])]).value
            else: # parent
                parent_products = self._context.get('parent_products')
                product_template = filter(
                    lambda x: x.get('product_tmpl_id') ==
                              self.bom_line_id.bom_id.product_tmpl_id.id,
                    parent_products)
                if product_template and len(product_template) == 1:
                    attribute_id = self.env['product.attribute'].search([(
                        'attribute_code','=', field_value[1])])
                    attribute_line = filter(lambda x: x[2]['attribute_id'] ==
                                          attribute_id.id,
                                   product_template[0][
                        'product_attribute_ids'])
                    if attribute_line and len(attribute_line) == 1:
                        attribute_value = attribute_line[0][2]['value_id']
                        value = self.env[
                            'product.attribute.value'].browse(attribute_value)
                        if value.attr_type == 'select':
                            try:
                                return float(value.name)
                            except ValueError:
                                return value.name
                        else: # numeric
                            return value.numeric_value
                else:
                    raise UserError(u'parent product not calculated yet')

        else:
            try:
                return float(field)
            except ValueError:
                for line in values:
                    if line.attribute_id.attribute_code == field:
                        if line.attribute_id.attr_type == 'select':
                            try:
                                return line.value_id and float(
                                    line.value_id.name)
                            except ValueError:
                                return line.value_id
                        elif line.attribute_id.attr_type == 'numeric':
                            return line.value_id and \
                                   line.value_id.numeric_value
                        elif line.attribute_id.attr_type == 'range':
                            return line.value_id and line.custom_value
                if re.compile('\s{2,}').search(field):
                    raise UserError(
                        _(u'check whitespaces on product line {} in '
                          u'conditions {}'.format(
                            field, self.bom_line_id.product_tmpl_id.name,
                            self.conditions)))
                else:
                    raise UserError(
                        _(u'no exist {} code on settled values on product '
                          u'line {} in conditions {}'.format(
                            field, self.bom_line_id.product_tmpl_id.name,
                            self.conditions)))


class MrpBomLineVariantSelector(models.Model):
    _name = 'mrp.bom.line.variant.selector'
    _inherit = 'mrp.bom.line.rule'

    attribute_id = fields.Many2one(
        comodel_name='product.attribute',
    )

    def _get_val(self, field, values):
        value_obj = self.env['product.attribute.value']
        field_value = field.split('.')
        # self.xx where 'xx' is value code of the attribute in the line
        if len(field_value) == 2 and field_value[0] in ['self', 'const',
                                                        'parent']:
            if field_value[0] == 'self':
                val = value_obj.search([(
                    'attribute_code', '=', field_value[1]),
                    ('attribute_id', '=', self.attribute_id.id)])
                if val.attribute_id.attr_type == 'select':
                    try:
                        return float(val.name)
                    except ValueError:
                        return val
                    except TypeError:
                        raise UserError(
                            u'Check attribute: {}, value: {}, numeric: {}'
                            u'\n'.format(val.attribute_id.name,
                                          val.name, val.numeric_value))
                elif val.attribute_id.attr_type == 'numeric':
                    return val.numeric_value
            elif field_value[0] == 'const':
                return self.env['mrp.constant'].search(
                    [('name', '=', field_value[1])]).value
            else: #field_value[0] == 'parent':
                parent_products = self._context.get('parent_products')
                product_template = filter(
                    lambda x: x.get('product_tmpl_id') ==
                              self.bom_line_id.bom_id.product_tmpl_id.id,
                    parent_products)
                if product_template and len(product_template) == 1:
                    attribute_id = self.env['product.attribute'].search([(
                        'attribute_code','=', field_value[1])])
                    attribute_line = filter(lambda x: x[2]['attribute_id'] ==
                                          attribute_id.id,
                                   product_template[0][
                        'product_attribute_ids'])
                    if attribute_line and len(attribute_line) == 1:
                        attribute_value = attribute_line[0][2]['value_id']
                        value = self.env[
                            'product.attribute.value'].browse(attribute_value)
                        if value.attr_type == 'select':
                            try:
                                return float(value.name)
                            except ValueError:
                                return value.name
                        else:  # numeric
                            return value.numeric_value
                else:
                    raise UserError(u'parent product not calculated yet')
        else:
            try:
                return float(field)
            except ValueError:
                for line in values:
                    if line.attribute_id.attribute_code == field:
                        if line.attribute_id.attr_type == 'select':
                            try:
                                return line.value_id and float(
                                    line.value_id.name)
                            except ValueError:
                                return value_obj.search([(
                                    'attribute_id', '=', self.attribute_id.id),
                                    ('name', '=', line.value_id.name)])
                        elif line.attribute_id.attr_type == 'numeric':
                            return line.value_id and \
                                   line.value_id.numeric_value
                        elif line.attribute_id.attr_type == 'range':
                            return line.value_id and line.custom_value
                raise UserError(
                    _(u'no exist {} code on settled values on product line {} '
                      u'attribute {} in conditions {}'.format(
                        field, self.bom_line_id.product_tmpl_id.name,
                        self.attribute_id.name, self.conditions)))
