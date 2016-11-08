# -*- coding: utf-8 -*-
# (c) 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestMrpRoutingCost(common.TransactionCase):

    def setUp(self):
        super(TestMrpRoutingCost, self).setUp()
        self.mrp_production = \
            self.env.ref('mrp_operations.mrp_production_op1')

    def test_compute_production_total(self):
        line = self.mrp_production.workcenter_lines[0]
        line.workcenter_op_number = 2
        line.workcenter_op_avg_cost = 21
        line.workcenter_cost_cycle = 15
        line.workcenter_cost_cycle = 12
        self.assertEqual(
            line.workcenter_op_subtotal,
            line.workcenter_id.op_avg_cost * line.workcenter_id.op_number)
        self.assertEqual(
            line.workcenter_subtotal_hour,
            line.hour * line.workcenter_id.costs_hour)
        line.workcenter_id.fixed_hour_cost = True
        self.assertEqual(
            line.workcenter_subtotal_hour, line.workcenter_id.costs_hour)
        self.assertEqual(line.workcenter_subtotal_cycle,
                         line.cycle * line.workcenter_id.costs_cycle)
        self.assertEqual(
            self.mrp_production.routing_cycle_total,
            sum(self.mrp_production.mapped(
                'workcenter_lines.workcenter_subtotal_cycle')))
        self.assertEqual(
            self.mrp_production.routing_hour_total,
            sum(self.mrp_production.mapped(
                'workcenter_lines.workcenter_subtotal_hour')))
        self.assertEqual(
            self.mrp_production.routing_operator_total,
            sum(self.mrp_production.mapped(
                'workcenter_lines.workcenter_op_subtotal')))
        self.assertEqual(line.unit_cost, line.workcenter_subtotal /
                         line.production_id.product_qty)
        self.assertEqual(self.mrp_production.routing_total,
                         self.mrp_production.routing_hour_total +
                         self.mrp_production.routing_cycle_total +
                         self.mrp_production.routing_operator_total)
