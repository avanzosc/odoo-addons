# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestStockPickingWithAnalyticProject(common.TransactionCase):

    def setUp(self):
        super(TestStockPickingWithAnalyticProject, self).setUp()
        picking_type = self.env['stock.picking.type'].search(
            [('code', '=', 'incoming')], limit=1)
        self.project = self.env['project.project'].create(
            {'name': 'Project stock picking with analytic account'})
        self.project.analytic_account_id.partner_id = (
            self.ref('base.res_partner_2'))
        self.product = self.browse_ref('product.consu_delivery_02')
        move_vals = {'product_id': self.product.id,
                     'name': self.product.name,
                     'quantity_done': 5.0,
                     'product_uom': self.product.uom_po_id.id,
                     'location_id':
                     picking_type.default_location_dest_id.location_id.id,
                     'location_dest_id':
                     picking_type.default_location_dest_id.id,
                     'picking_type_id': picking_type.id}
        picking_vals = {'analytic_account_id':
                        self.project.analytic_account_id.id,
                        'location_id':
                        picking_type.default_location_dest_id.location_id.id,
                        'location_dest_id':
                        picking_type.default_location_dest_id.id,
                        'picking_type_id': picking_type.id,
                        'move_lines': [(0, 0, move_vals)]}
        self.picking = self.env['stock.picking'].create(picking_vals)

    def test_stock_picking_with_analytic_account(self):
        self.picking.onchange_analytic_account_id()
        self.assertEqual(
            self.picking.partner_id.id,
            self.picking.analytic_account_id.partner_id.id,
            'BAD partner in stock picking')
        self.project._compute_picking_count()
        self.assertEqual(
            self.project.picking_count, 1, 'BAD picking number for project')
        result = self.project.show_pickings_from_project()
        domain = "[('id', 'in', [{}])]".format(self.picking.id)
        self.assertEqual(
            str(result.get('domain')), domain, 'BAD domain from project')
        self.project.analytic_account_id._compute_picking_count()
        self.assertEqual(
            self.project.analytic_account_id.picking_count, 1,
            'BAD picking number for analytic account')
        account = self.project.analytic_account_id
        result = account.show_pickings_from_analytic_account()
        domain = "[('id', 'in', [{}])]".format(self.picking.id)
        self.assertEqual(
            str(result.get('domain')), domain,
            'BAD domain from analytic account')
        self.picking.button_validate()
        cond = [('account_id', '=', account.id)]
        analytic_line = self.env['account.analytic.line'].search(cond, limit=1)
        self.assertEqual(
            len(analytic_line), 1, 'Analytic line not generated')
