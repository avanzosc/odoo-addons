# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestResPartnerShowOnlyName(common.TransactionCase):

    def setUp(self):
        super(TestResPartnerShowOnlyName, self).setUp()
        self.partner_model = self.env['res.partner']
        vals = {'name': 'Alfredo',
                'parent_id': self.ref('base.res_partner_2'),
                'customer': True,
                'active': True}
        self.partner = self.partner_model.create(vals)

    def test_res_partnerShowOnlyName(self):
        res = self.partner_model.name_search(
            'Alfredo', args=[], operator='ilike', limit=8)
        self.assertNotEqual(
            len(res), 0, 'Partner name not found')
        self.assertEqual(
            res[0][1], 'Alfredo', 'Alfredo name not found')
