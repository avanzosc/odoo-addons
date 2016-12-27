# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
import time
from openerp import fields


class TestStockInformation(common.TransactionCase):

    def setUp(self):
        super(TestStockInformation, self).setUp()
        self.stock_information_model = self.env['stock.information']
        self.wiz_model = self.env['wiz.stock.information']
        self.wiz_create_model = self.env['wiz.create.procurement.stock.info']
        self.wiz_run_model = self.env['wiz.run.procurement.stock.info']
        year = time.strftime("%Y")
        to_date = str(year) + '-12-31'
        wiz_vals = {'company': self.ref('base.main_company'),
                    'to_date': to_date}
        self.wiz = self.wiz_model.create(wiz_vals)

    def test_stock_information(self):
        self.wiz.calculate_stock_information()
        cond = []
        informations = self.stock_information_model.search(cond)
        self.assertNotEqual(
            len(informations), 0, 'Stock information no generated')
        for information in informations:
            information.show_incoming_pending_purchases()
            information.show_incoming_pending_moves()
            information.show_outgoing_pending_moves()
            information.show_demand_procurements()
            information.show_draft_purchases()
            information.show_draft_sales()
            information_date = fields.Datetime.from_string(
                information.last_day_week).date()
            information._calculate_first_day_week(information_date)
        wiz_create = self.wiz_create_model.create({})
        wiz_create.with_context(
            {'active_ids': informations.ids}).create_procurement_orders()
        wiz_run = self.wiz_run_model.create({})
        wiz_run.with_context(
            {'active_ids': informations.ids}).run_procurement_orders()
