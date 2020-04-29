# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo.exceptions import UserError


@common.at_install(False)
@common.post_install(True)
class TestStockUsability(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockUsability, cls).setUpClass()
        cls.picking_type_model = cls.env['stock.picking.type']
        cls.location_model = cls.env['stock.location']
        cls.picking_model = cls.env['stock.picking']
        cls.partner_model = cls.env['res.partner']
        cls.wiz_model = cls.env['stock.immediate.transfer']

    def test_stock_usability(self):
        cond = [('picking_type_code', '=', 'outgoing'),
                ('state', '=', 'draft')]
        picking = self.picking_model.search(cond, limit=1)
        self.assertEquals(picking.move_lines[0].state, 'draft')
        picking.move_lines[0].stock_usability_action_confirm()
        self.assertEquals(picking.move_lines[0].state, 'confirmed')
        picking.move_lines[0].stock_usability_action_cancel()
        self.assertEquals(picking.move_lines[0].state, 'cancel')
        picking.move_lines[0].stock_usability_action_to_draft()
        self.assertEquals(picking.move_lines[0].state, 'draft')
        picking.move_lines[0].stock_usability_action_confirm()
        self.assertEquals(picking.move_lines[0].state, 'confirmed')
        cond = [('supplier', '=', True)]
        supplier = self.partner_model.search(cond, limit=1)
        cond = [('code', '=', 'incoming')]
        in_picking_type = self.picking_type_model.search(
            cond, limit=1)
        location_supplier = self.location_model.search(
            [('usage', '=', 'supplier')], limit=1)
        picking_vals = {
            'partner_id': supplier.id,
            'picking_type_id': in_picking_type.id,
            'location_id': location_supplier.id,
            'location_dest_id': in_picking_type.default_location_dest_id.id}
        picking_line_vals = {
            'product_id': picking.move_lines[0].product_id.id,
            'name': picking.move_lines[0].product_id.name,
            'product_uom_qty': 100,
            'product_uom': picking.move_lines[0].product_id.uom_id.id}
        picking_vals['move_lines'] = [(0, 0, picking_line_vals)]
        picking2 = self.picking_model.create(picking_vals)
        picking2.action_confirm()
        wizard_vals = {'pick_ids': [(6, 0, picking2.ids)]}
        wizard = self.wiz_model.create(wizard_vals)
        wizard.process()
        picking.move_lines[0].stock_usability_action_assign()
        self.assertEquals(picking.move_lines[0].state, 'assigned')
        picking.move_lines[0].stock_usability_do_unreserve()
        self.assertEquals(picking.move_lines[0].state, 'confirmed')
        picking.move_lines[0].stock_usability_action_assign()
        picking.move_lines[0].product_id.tracking = 'lot'
        with self.assertRaises(UserError):
            picking.move_lines[0].stock_usability_button_validate()
        picking.move_lines[0].product_id.tracking = 'none'
        picking.move_lines[0].stock_usability_button_validate()
        self.assertEquals(picking.move_lines[0].state, 'done')

    def test_stock_usability_errors(self):
        cond = [('picking_type_code', '=', 'outgoing'),
                ('state', '=', 'draft')]
        picking = self.picking_model.search(cond, limit=1)
        self.assertEquals(picking.move_lines[0].state, 'draft')
        picking.move_lines[0].stock_usability_action_confirm()
        self.assertEquals(picking.move_lines[0].state, 'confirmed')
        cond = [('supplier', '=', True)]
        supplier = self.partner_model.search(cond, limit=1)
        cond = [('code', '=', 'incoming')]
        in_picking_type = self.picking_type_model.search(
            cond, limit=1)
        location_supplier = self.location_model.search(
            [('usage', '=', 'supplier')], limit=1)
        picking_vals = {
            'partner_id': supplier.id,
            'picking_type_id': in_picking_type.id,
            'location_id': location_supplier.id,
            'location_dest_id': in_picking_type.default_location_dest_id.id}
        picking_line_vals = {
            'product_id': picking.move_lines[0].product_id.id,
            'name': picking.move_lines[0].product_id.name,
            'product_uom_qty': 100,
            'product_uom': picking.move_lines[0].product_id.uom_id.id}
        picking_vals['move_lines'] = [(0, 0, picking_line_vals)]
        picking2 = self.picking_model.create(picking_vals)
        picking2.action_confirm()
        wizard_vals = {'pick_ids': [(6, 0, picking2.ids)]}
        wizard = self.wiz_model.create(wizard_vals)
        wizard.process()
        picking.move_lines[0].stock_usability_action_assign()
        self.assertEquals(picking.move_lines[0].state, 'assigned')
        picking.move_lines[0].stock_usability_do_unreserve()
        self.assertEquals(picking.move_lines[0].state, 'confirmed')
        picking.move_lines[0].stock_usability_action_assign()
        picking.move_line_ids.unlink()
        with self.assertRaises(UserError):
            picking.move_lines[0].stock_usability_button_validate()
