# -*- coding: utf-8 -*-
# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.addons.stock_quant_manual_assign.tests\
    .test_stock_quant_manual_assign import TestStockQuantManualAssign


class TestStockQuantManualAssignBackorder(TestStockQuantManualAssign):

    def setUp(self):
        super(TestStockQuantManualAssignBackorder, self).setUp()
        self.picking_model = self.env['stock.picking']
        self.picking = self.picking_model.create({
            'partner_id': self.env.ref('base.partner_root').id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
        })
        self.move.write({
            'picking_id': self.picking.id,
        })
        self.move.action_confirm()

    def test_partial_picking(self):
        wizard = self.quant_assign_wizard.with_context(
            active_id=self.move.id).create({
                'name': 'New wizard',
            })
        wizard.quants_lines[0].write({
            'selected': True,
        })
        wizard.quants_lines[0].onchange_selected()
        wizard.quants_lines[1].write({
            'selected': True,
            'qty': 50.0,
        })
        wizard.assign_quants()
        selected_quants = wizard.quants_lines.filtered(
            'selected').mapped('quant')
        for quant in self.move.reserved_quant_ids:
            self.assertTrue(quant in selected_quants)
        self.picking.do_prepare_partial()
        self.picking.pack_operation_ids.filtered(
            lambda o: o.location_id != self.location1).unlink()
        not_transferred_quants = (
            selected_quants.filtered(
                lambda q: q.location_id != self.location1))
        self.picking.do_transfer()
        backorder = self.picking_model.search([
            ('backorder_id', '=', self.picking.id)])
        self.assertTrue(backorder)
        self.assertTrue(not_transferred_quants in backorder.mapped(
            'move_lines.reserved_quant_ids'))
