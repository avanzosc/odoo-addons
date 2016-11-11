# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import TransactionCase


class TestMrpRoutingCost(TransactionCase):

    def setUp(self):
        super(TestMrpRoutingCost, self).setUp()
        self.mrp_production_model = self.env['mrp.production']
        self.bom_model = self.env['mrp.bom']
        self.routing_model = self.env['mrp.routing']
        self.product_model = self.env['product.product']
        workcenter = self.env['mrp.workcenter'].create({
            'name': 'Workcenter',
            'resource_type': 'material',
            'op_avg_cost': 7.0,
            'op_number': 3.0,
            'costs_hour': 15.0,
            'costs_cycle': 12.0,
        })
        unit_id = self.ref('product.product_uom_unit')
        dozen_id = self.ref('product.product_uom_dozen')
        bom_product = self.product_model.create({
            'name': 'BoM product',
            'uom_id': unit_id,
        })
        self.component1 = self.product_model.create({
            'name': 'Component1',
            'standard_price': 10.0,
            'uom_id': dozen_id,
        })
        self.component2 = self.product_model.create({
            'name': 'Component2',
            'standard_price': 15.0,
            'uom_id': unit_id,
        })
        vals = {
            'product_tmpl_id': bom_product.product_tmpl_id.id,
            'product_id': bom_product.id,
            'bom_line_ids':
                [(0, 0, {'product_id': self.component1.id,
                         'product_qty': 2.0}),
                 (0, 0, {'product_id': self.component2.id,
                         'product_qty': 12.0})],
        }
        self.mrp_bom = self.bom_model.create(vals)
        vals = {
            'name': 'Routing Test',
            'workcenter_lines':
                [(0, 0, {'name': 'Routing Workcenter',
                         'do_production': True,
                         'workcenter_id': workcenter.id,
                         })],
        }
        self.routing = self.routing_model.create(vals)
        self.production = self.mrp_production_model.create({
            'product_id': bom_product.id,
            'product_uom': bom_product.uom_id.id,
            'bom_id': self.mrp_bom.id,
            'routing_id': self.routing.id,
        })

    def test_compute_production_total(self):
        self.production.action_compute()
        for line in self.production.workcenter_lines:
            self.assertEqual(
                round(line.subtotal_operator, 2),
                round(line.workcenter_id.op_avg_cost *
                      line.workcenter_id.op_number, 2))
            self.assertEqual(
                round(line.subtotal_cycle, 2),
                round(line.cycle * line.workcenter_id.costs_cycle, 2))
            line.workcenter_id.fixed_cycle_cost = True
            self.assertEqual(
                round(line.subtotal_cycle, 2),
                round(line.workcenter_id.costs_cycle, 2))
            self.assertEqual(
                round(line.subtotal_hour, 2),
                round(line.hour * line.workcenter_id.costs_hour, 2))
            line.workcenter_id.fixed_hour_cost = True
            self.assertEqual(
                round(line.subtotal_hour, 2),
                round(line.workcenter_id.costs_hour, 2))
            self.assertEqual(
                round(line.unit_final_cost, 2),
                round(line.subtotal / line.production_id.product_qty, 2))
        self.assertEqual(
            self.production.routing_cycle_total,
            sum(self.production.mapped(
                'workcenter_lines.subtotal_cycle')))
        self.assertEqual(
            self.production.routing_hour_total,
            sum(self.production.mapped(
                'workcenter_lines.subtotal_hour')))
        self.assertEqual(
            self.production.routing_operator_total,
            sum(self.production.mapped(
                'workcenter_lines.subtotal_operator')))

    def test_workorder_line_onchange_workcenter_id(self):
        self.production.action_compute()
        for line in self.production.workcenter_lines:
            self.assertEquals(round(line.op_avg_cost, 2),
                              round(line.workcenter_id.op_avg_cost, 2))
            self.assertEquals(round(line.op_number, 2),
                              round(line.workcenter_id.op_number, 2))
            self.assertEquals(round(line.costs_hour, 2),
                              round(line.workcenter_id.costs_hour, 2))
            self.assertEquals(round(line.costs_cycle, 2),
                              round(line.workcenter_id.costs_cycle, 2))
            line.write({
                'op_avg_cost': 8.0,
                'op_number': 4.0,
                'costs_hour': 16.0,
                'costs_cycle': 11.0,
            })
            self.assertNotEquals(round(line.op_avg_cost, 2),
                                 round(line.workcenter_id.op_avg_cost, 2))
            self.assertNotEquals(round(line.op_number, 2),
                                 round(line.workcenter_id.op_number, 2))
            self.assertNotEquals(round(line.costs_hour, 2),
                                 round(line.workcenter_id.costs_hour, 2))
            self.assertNotEquals(round(line.costs_cycle, 2),
                                 round(line.workcenter_id.costs_cycle, 2))
            line.onchange_workcenter_id()
            self.assertEquals(round(line.op_avg_cost, 2),
                              round(line.workcenter_id.op_avg_cost, 2))
            self.assertEquals(round(line.op_number, 2),
                              round(line.workcenter_id.op_number, 2))
            self.assertEquals(round(line.costs_hour, 2),
                              round(line.workcenter_id.costs_hour, 2))
            self.assertEquals(round(line.costs_cycle, 2),
                              round(line.workcenter_id.costs_cycle, 2))
