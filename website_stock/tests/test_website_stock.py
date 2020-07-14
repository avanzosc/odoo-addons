# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestWebsiteStock(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestWebsiteStock, cls).setUpClass()
        cls.stock_picking_model = cls.env['stock.picking']
        picking_type = cls.env.ref('stock.picking_type_in')
        location = cls.env['stock.location'].search([], limit=1)

        cls.stock_picking_1 = cls.stock_picking_model.create({
            'picking_type_id': picking_type.id,
            'location_id': location.id,
            'location_dest_id': location.id
        })

    def test_website_stock(self):
        self.stock_picking_1._get_report_base_filename()
        self.stock_picking_1._compute_access_url()

        be_signed = self.stock_picking_1.has_to_be_signed()
        self.assertEquals(be_signed, True)
        self.stock_picking_1.write({
            'state': 'done'
            })
        be_signed = self.stock_picking_1.has_to_be_signed()
        self.assertEquals(be_signed, False)
