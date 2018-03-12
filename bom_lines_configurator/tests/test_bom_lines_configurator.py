# -*- coding: utf-8 -*-
# © 2017 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.tests.common import TransactionCase


class TestMrpBomConfigurator(TransactionCase):
    def setUp(self):
        super(TestMrpBomConfigurator, self).setUp()
        self.tmpl_model = self.env['product.template'].with_context(
            check_variant_creation=True)
        self.categ_model = self.env['product.category']
        self.attr_obj = self.env['product.attribute']
        self.value_obj = self.env['product.attribute.value']
        self.bom_model = self.env['mrp.bom']
        self.production_model = self.env['mrp.production']
        self.categ1 = self.categ_model.create({
            'name': 'No create variants category',
        })
        self.categ2 = self.categ_model.create({
            'name': 'Create variants category',
            'no_create_variants': False,
        })
        self.attribute = self.attr_obj.create({
            'name': 'Test Attribute',
            'attribute_code': 'attr1',
            'attr_type': 'select'
        })
        self.attribute2 = self.attr_obj.create({
            'name': 'Test Attribute 2',
            'attribute_code': 'attr2',
            'attr_type': 'numeric',
        })
        self.attribute3 = self.attr_obj.create({
            'name': 'Test Attribute 3',
            'attribute_code': 'attr3',
            'attr_type': 'range',
        })
        self.value1 = self.value_obj.create({
            'name': 'Value 1',
            'attribute_id': self.attribute.id,
            'attribute_code': 'val1'
        })
        self.value2 = self.value_obj.create({
            'name': '2',
            'attribute_id': self.attribute.id,
            'attribute_code': 'val2'
        })
        self.value3 = self.value_obj.create({
            'name': 'Value 3',
            'attribute_id': self.attribute2.id,
            'attribute_code': 'val3',
            'numeric_value': 3,
        })
        self.value4 = self.value_obj.create({
            'name': 'Value 4',
            'attribute_id': self.attribute2.id,
            'attribute_code': 'val3',
            'numeric_value': 4,
        })
        self.value5 = self.value_obj.create({
            'name': 'Value 5',
            'attribute_id': self.attribute3.id,
            'attribute_code': 'val5',
            'min_range': 0,
            'max_range': 9,
        })
        self.value6 = self.value_obj.create({
            'name': 'Value ',
            'attribute_id': self.attribute3.id,
            'attribute_code': 'val6',
            'min_range': 10,
            'max_range': 19,
        })

        self.template = self.tmpl_model.create({
            'name': 'Category option template',
            'categ_id': self.categ2.id,
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.attribute.id,
                        'value_ids': [(6, 0, [self.value1.id,
                                              self.value2.id])]}),
                (0, 0, {'attribute_id': self.attribute2.id, 'value_ids':
                    [(6, 0, [self.value3.id, self.value4.id])]}),
                (0, 0, {'attribute_id': self.attribute3.id, 'value_ids':
                    [(6, 0, [self.value5.id, self.value6.id])]})
            ],
        })

        self.component_attribute1 = self.attr_obj.create({
            'name': 'Test Component Attribute',
            'attribute_code': 'comp_attr1',
            'attr_type': 'numeric',
        })
        self.component_attribute2 = self.attr_obj.create({
            'name': 'Test Component Attribute 2',
            'attribute_code': 'comp_attr2',
            'attr_type': 'numeric',
        })
        self.component_attribute3 = self.attr_obj.create({
            'name': 'Test Component Attribute 3',
            'attribute_code': 'comp_attr3',
            'attr_type': 'select',
        })
        self.component_value1 = self.value_obj.create({
            'name': 'Component Value 1',
            'attribute_id': self.component_attribute1.id,
            'attribute_code': 'comp_val1',
            'numeric_value': 2,
        })
        self.component_value2 = self.value_obj.create({
            'name': 'Component Value 2',
            'attribute_id': self.component_attribute1.id,
            'attribute_code': 'comp_val2',
            'numeric_value': 5,
        })
        self.component_value3 = self.value_obj.create({
            'name': 'Component Value 3',
            'attribute_id': self.component_attribute2.id,
            'attribute_code': 'comp_val3',
            'numeric_value': 5,
        })
        self.component_value4 = self.value_obj.create({
            'name': 'Component Value 4',
            'attribute_id': self.component_attribute2.id,
            'attribute_code': 'comp_val4',
            'numeric_value': 11,
        })
        self.component_value5 = self.value_obj.create({
            'name': 'Component Value 5',
            'attribute_id': self.component_attribute3.id,
            'attribute_code': 'comp_val5',
        })
        self.component1 = self.tmpl_model.create({
            'name': 'Component 1',
            'categ_id': self.categ2.id,
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.component_attribute1.id,
                        'value_ids': [(6, 0, [self.component_value1.id,
                                              self.component_value2.id])]})],
        })
        self.component2 = self.tmpl_model.create({
            'name': 'Component 2',
            'categ_id': self.categ2.id,
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.component_attribute2.id,
                        'value_ids': [(6, 0, [self.component_value3.id,
                                              self.component_value4.id])]})],
        })
        self.component3 = self.tmpl_model.create({
            'name': 'Component 3',
            'categ_id': self.categ2.id,
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.component_attribute1.id,
                        'value_ids': [(6, 0, [self.component_value1.id,
                                              self.component_value2.id])]})],
        })
        rule_line1 = {'attribute_id': self.component_attribute1.id,
                      'formula_qty': 'attr1',
                      'conditions': '[True]'}
        qty_rule_line1 = {'formula_qty': '2',
                          'conditions': '[True]'}
        rule_line2 = {'attribute_id': self.component_attribute1.id,
                      'formula_qty': 'attr2 2 +',
                      'conditions': '[True]'}
        qty_rule_line2 = {'formula_qty': 'attr2',
                          'conditions': '[True]'}
        rule_line3 = {'attribute_id': self.component_attribute2.id,
                      'formula_qty': 'attr3 5 +', # custom value 6!!!!
                      'conditions': '[True]'}
        qty_rule_line3 = {'formula_qty': 'attr2',
                          'conditions': '[True]'}

        master_bom_bom_line_ids = [
            (0, 0, {'product_tmpl_id': self.component1.id,
                    'type': 'normal',
                    'product_qty': 1,
                    'product_uom': self.component1.uom_id.id,
                    'attribute_selections_ids': [(0, 0, rule_line2)],
                    'attribute_rule_ids': [(0, 0, qty_rule_line2)],
                    }),
            (0, 0, {'product_tmpl_id': self.component2.id,
                    'type': 'phantom',
                    'product_qty': 1,
                    'product_uom': self.component2.uom_id.id,
                    'attribute_selections_ids': [(0, 0, rule_line3)],
                    'attribute_rule_ids': [(0, 0, qty_rule_line3)],
                    })
        ]
        self.master_bom = self.bom_model.create({
            'name': 'Template BoM',
            'product_tmpl_id': self.template.id,
            'product_qty': 3.0,
            'product_uom': self.template.uom_id.id,
            'type': 'normal',
            'bom_line_ids': master_bom_bom_line_ids
        })

        self.phantom_bom = self.bom_model.create({
            'name': 'Template BoM',
            'product_tmpl_id': self.component2.id,
            'product_qty': 1.0,
            'product_uom': self.component2.uom_id.id,
            'type': 'normal',
            'bom_line_ids': [(0, 0, {'product_tmpl_id': self.component3.id,
                                     'type': 'normal',
                                     'product_qty': 2,
                                     'product_uom': self.component3.uom_id.id,
                                     'attribute_selection_ids': [(0, 0,
                                                                 rule_line1)],
                                     'attribute_rule_ids': [(0, 0,
                                                             qty_rule_line1)]
                                     })]
        })

        production_product_attribute_ids = [
            (0, 0, {'attribute_id': self.attribute.id, 'value_id':
                self.value2.id, 'owner_model': 'mrp.production',
                    'product_tmpl_id': self.template.id}),
            (0, 0, {'attribute_id': self.attribute2.id, 'value_id':
                self.value3.id, 'owner_model': 'mrp.production',
                    'product_tmpl_id': self.template.id}),
            (0, 0, {'attribute_id': self.attribute3.id, 'value_id':
                self.value5.id, 'custom_value': 6,
                    'owner_model': 'mrp.production', 'product_tmpl_id':
                        self.template.id}),
        ]
        self.production = self.production_model.create({
            'product_tmpl_id': self.template.id,
            'product_qty': 50.0,
            'product_uom': self.template.uom_id.id,
            'bom_id': self.master_bom.id,
            'product_attribute_ids': production_product_attribute_ids
        })

    def test_bom_lines_configurator(self):
        self.production.action_compute()
        pass