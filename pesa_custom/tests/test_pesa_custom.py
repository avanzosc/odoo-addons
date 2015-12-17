# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestPesaCustom(common.TransactionCase):

    def setUp(self):
        super(TestPesaCustom, self).setUp()
        self.schedule_model = self.env['schedule']

    def test_name_search(self):
        self.schedule1 = self.schedule_model.create({'hour': 16.5})
        res = self.schedule1.name_get()
        self.assertEqual([x[1] for x in res][0], '16:30',
                         'Schedule is not the same')
