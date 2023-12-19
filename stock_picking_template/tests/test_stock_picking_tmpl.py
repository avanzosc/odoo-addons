# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo import fields


class TestStockPickingTemplate(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockPickingTemplate, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.move_model = cls.env['stock.move']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.wiz_tmpl = cls.env['stock.picking.duplicate']
        cls.picking_model = cls.env['stock.picking']
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.supplier_location = cls.env.ref(
            'stock.stock_location_suppliers')
        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.picking_type_in = cls.env[
            'ir.model.data'].xmlid_to_res_id('stock.picking_type_in')
        cls.product = cls.product_model.create({
            'name': 'Product',
            'type': 'product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'tracking': 'serial',
        })

    def test_duplicate_from_picking(self):
        self.picking1 = self.picking_model.create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type_in,
            'location_id': self.supplier_location.id,
            'location_dest_id': self.stock_location.id})
        self.move_model.create({
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom_qty': 2,
            'product_uom': self.product.uom_id.id,
            'picking_id': self.picking1.id,
            'location_id': self.supplier_location.id,
            'location_dest_id': self.stock_location.id})
        pick_ids = self.picking_model.search([('partner_id', '=',
                                               self.partner.id)]).ids
        self.assertEqual(len(pick_ids), 1, 'BAD picking number')
        today = fields.Date.to_string(fields.Date.today())
        wiz_vals = {'scheduled_date': today}
        wizard = self.wiz_tmpl.create(wiz_vals)
        res = wizard.with_context(active_ids=[]).duplicate_picking()
        self.assertEqual(res, {'type': 'ir.actions.act_window_close'},
                         'BAD return')
        wizard.with_context(active_ids=[self.picking1.id]).duplicate_picking()
        new_pick_ids = self.picking_model.search([('partner_id', '=',
                                                   self.partner.id)]).ids
        self.assertEqual(len(new_pick_ids), 2, 'BAD picking number')
        new_pick_ids.remove(pick_ids[0])
        new_pick = self.picking_model.browse(new_pick_ids[0])
        self.assertEqual(fields.Date.to_string(new_pick.scheduled_date),
                         today, 'BAD picking date')
