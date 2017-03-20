# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common
from openerp import fields

from datetime import timedelta


class TestMrpProductionMerge(common.TransactionCase):

    def setUp(self):
        super(TestMrpProductionMerge, self).setUp()
        self.production_model = self.env['mrp.production']
        product_model = self.env['product.product']
        uom_model = self.env['product.uom']
        bom_model = self.env['mrp.bom']
        routing_model = self.env['mrp.routing']
        self.merge_model = self.env['mrp.production.merge']
        self.today = fields.Datetime.now()
        self.tomorrow =\
            fields.Datetime.from_string(self.today) + timedelta(days=1)
        self.yesterday = \
            fields.Datetime.from_string(self.today) - timedelta(days=1)
        uom_categ = self.env['product.uom.categ'].create({
            'name': 'UoM category',
        })
        self.uom1 = uom_model.create({
            'name': 'One Unit',
            'category_id': uom_categ.id,
        })
        self.uom2 = uom_model.create({
            'name': 'Two Unit',
            'category_id': uom_categ.id,
            'uom_type': 'bigger',
            'factor': 2,
        })
        self.product1 = product_model.create({
            'name': 'Product 1',
            'uom_id': self.uom1.id,
            'uom_po_id': self.uom1.id,
        })
        self.product2 = product_model.create({
            'name': 'Product 2',
            'uom_id': self.uom1.id,
            'uom_po_id': self.uom1.id,
        })
        self.routing1 = routing_model.create({
            'name': 'Routing 1',
        })
        self.routing2 = routing_model.create({
            'name': 'Routing 2',
        })
        self.bom1 = bom_model.create({
            'product_id': self.product1.id,
            'product_tmpl_id': self.product1.product_tmpl_id.id,
            'product_uom': self.uom1.id,
            'routing_id': self.routing1.id,
        })
        self.bom2 = bom_model.create({
            'product_id': self.product1.id,
            'product_tmpl_id': self.product1.product_tmpl_id.id,
            'product_uom': self.uom1.id,
        })
        self.mo1 = self.production_model.create({
            'product_id': self.product1.id,
            'product_uom': self.product1.uom_id.id,
            'date_planned': self.today,
            'bom_id': self.bom1.id,
            'routing_id': self.bom1.routing_id.id,
        })

    def test_merge_correct(self):
        mo2 = self.production_model.create({
            'product_id': self.mo1.product_id.id,
            'product_qty': self.mo1.product_qty,
            'product_uom': self.mo1.product_uom.id,
            'bom_id': self.mo1.bom_id.id,
            'routing_id': self.mo1.routing_id.id,
            'date_planned': self.tomorrow,
        })
        orders = self.mo1 | mo2
        merge = self.merge_model.with_context(
            active_model='mrp.production', active_ids=orders.ids).create({})
        self.assertTrue(merge.line_ids)
        self.assertEquals(
            merge.line_ids[:1].product_qty, sum(orders.mapped('product_qty')))
        self.assertEquals(
            merge.line_ids[:1].date_planned,
            min(orders.mapped('date_planned')))
        self.assertEquals(merge.line_ids[:1].date_planned, self.today)
        merge.line_ids.write({'date_planned': self.yesterday})
        merge.merge_manufacturing_orders_button()
        self.assertEquals(orders[:1].state, 'draft')
        self.assertEquals(orders[:1].date_planned,
                          fields.Datetime.to_string(self.yesterday))
        for state in orders[1:].mapped('state'):
            self.assertEquals(state, 'cancel')

    def test_merge_correct_one_norouting(self):
        mo2 = self.production_model.create({
            'product_id': self.mo1.product_id.id,
            'product_qty': self.mo1.product_qty,
            'product_uom': self.mo1.product_uom.id,
            'bom_id': self.mo1.bom_id.id,
            'date_planned': self.tomorrow,
        })
        orders = self.mo1 | mo2
        merge = self.merge_model.with_context(
            active_model='mrp.production', active_ids=orders.ids).create({})
        self.assertTrue(merge.line_ids)
        self.assertEquals(
            merge.line_ids[:1].product_qty, sum(orders.mapped('product_qty')))
        self.assertEquals(
            merge.line_ids[:1].date_planned,
            min(orders.mapped('date_planned')))
        self.assertEquals(merge.line_ids[:1].date_planned, self.today)

    def test_merge_correct_both_norouting(self):
        self.bom1.routing_id = False
        self.mo1.routing_id = False
        mo2 = self.production_model.create({
            'product_id': self.mo1.product_id.id,
            'product_qty': self.mo1.product_qty,
            'product_uom': self.mo1.product_uom.id,
            'bom_id': self.mo1.bom_id.id,
            'date_planned': self.tomorrow,
        })
        orders = self.mo1 | mo2
        merge = self.merge_model.with_context(
            active_model='mrp.production', active_ids=orders.ids).create({})
        self.assertTrue(merge.line_ids)
        self.assertEquals(
            merge.line_ids[:1].product_qty, sum(orders.mapped('product_qty')))
        self.assertEquals(
            merge.line_ids[:1].date_planned,
            min(orders.mapped('date_planned')))
        self.assertEquals(merge.line_ids[:1].date_planned, self.today)

    def test_merge_wrong_routing(self):
        self.bom1.routing_id = False
        mo2 = self.production_model.create({
            'product_id': self.mo1.product_id.id,
            'product_qty': self.mo1.product_qty,
            'product_uom': self.mo1.product_uom.id,
            'bom_id': self.mo1.bom_id.id,
            'date_planned': self.tomorrow,
        })
        orders = self.mo1 | mo2
        merge = self.merge_model.with_context(
            active_model='mrp.production', active_ids=orders.ids).create({})
        self.assertFalse(merge.line_ids)

    def test_merge_wrong_routing2(self):
        mo2 = self.production_model.create({
            'product_id': self.mo1.product_id.id,
            'product_qty': self.mo1.product_qty,
            'product_uom': self.mo1.product_uom.id,
            'bom_id': self.mo1.bom_id.id,
            'routing_id': self.routing2.id,
            'date_planned': self.tomorrow,
        })
        orders = self.mo1 | mo2
        merge = self.merge_model.with_context(
            active_model='mrp.production', active_ids=orders.ids).create({})
        self.assertFalse(merge.line_ids)

    def test_merge_wrong_bom(self):
        mo2 = self.production_model.create({
            'product_id': self.mo1.product_id.id,
            'product_qty': self.mo1.product_qty,
            'product_uom': self.mo1.product_uom.id,
            'bom_id': self.bom2.id,
            'routing_id': self.mo1.routing_id.id,
            'date_planned': self.tomorrow,
        })
        orders = self.mo1 | mo2
        merge = self.merge_model.with_context(
            active_model='mrp.production', active_ids=orders.ids).create({})
        self.assertFalse(merge.line_ids)

    def test_merge_wrong_uom(self):
        mo2 = self.production_model.create({
            'product_id': self.mo1.product_id.id,
            'product_qty': self.mo1.product_qty,
            'product_uom': self.uom2.id,
            'bom_id': self.mo1.bom_id.id,
            'routing_id': self.mo1.routing_id.id,
            'date_planned': self.tomorrow,
        })
        orders = self.mo1 | mo2
        merge = self.merge_model.with_context(
            active_model='mrp.production', active_ids=orders.ids).create({})
        self.assertFalse(merge.line_ids)

    def test_merge_wrong_product(self):
        mo2 = self.production_model.create({
            'product_id': self.product2.id,
            'product_qty': self.mo1.product_qty,
            'product_uom': self.mo1.product_uom.id,
            'bom_id': self.mo1.bom_id.id,
            'routing_id': self.mo1.routing_id.id,
            'date_planned': self.tomorrow,
        })
        orders = self.mo1 | mo2
        merge = self.merge_model.with_context(
            active_model='mrp.production', active_ids=orders.ids).create({})
        self.assertFalse(merge.line_ids)
