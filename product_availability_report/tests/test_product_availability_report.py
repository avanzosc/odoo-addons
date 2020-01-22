# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestProductAvailabilityReport(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductAvailabilityReport, cls).setUpClass()
        cls.wiz_model = cls.env['stock.immediate.transfer']
        cls.picking_model = cls.env['stock.picking']

    def test_product_availability_report(self):
        cond = [('state', '=', 'assigned'),
                ('location_id.usage', '=', 'internal')]
        pickings = self.picking_model.search(cond)
        for p in pickings:
            if p.move_lines[0].reserved_availability > 0:
                picking = p
        picking.move_lines[0]._compute_entry_out_expected_amount()
        picking.move_lines[0]._compute_reserved_availability_amount()
        self.assertEqual(picking.move_lines[0].entry_amount, 0.0)
        self.assertEqual(picking.move_lines[0].out_amount,
                         picking.move_lines[0].product_uom_qty * -1)
        self.assertEqual(picking.move_lines[0].expected_amount,
                         picking.move_lines[0].product_uom_qty * -1)
        self.assertEqual(
            picking.move_lines[0].reserved_availability_amount,
            picking.move_lines[0].reserved_availability)
