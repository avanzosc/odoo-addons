# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestQcInspectionFromPartner(common.TransactionCase):

    def setUp(self):
        super(TestQcInspectionFromPartner, self).setUp()
        self.inspection_model = self.env['qc.inspection']
        inspection_vals = {'object_id': ('res.partner,' +
                                         str(self.ref('base.res_partner_2')))}
        self.inspection = self.inspection_model.create(inspection_vals)

    def test_qc_inspection_from_partner(self):
        self.env.ref('base.res_partner_2').inspections_from_partner()
        self.assertNotEqual(
            self.env.ref('base.res_partner_2').inspections_count, 0,
            'Partner without inspections')
