# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestResPartnerShowOnlyName(common.TransactionCase):

    def setUp(self):
        super(TestResPartnerShowOnlyName, self).setUp()
        self.partner_model = self.env['res.partner']
        self.partner = self.env.ref('base.res_partner_address_23')

    def test_res_partner_show_address(self):
        res_get = self.partner.name_get()[0][1]
        name_get = self.partner.with_context(
            show_address=True).name_get()[0][1]
        address = name_get.split("\n")[1:]
        res = self.partner_model.name_search(
            res_get, args=[], operator='ilike', limit=8)
        self.assertEqual(
            self.partner.name_get()[0][1], self.partner.name)
        self.assertEqual(
            res[0][1], self.partner.name, 'Angel Cook name not found')
        self.assertEqual(address[0], self.partner.street)

    def test_res_partner_show_email(self):
        email_get = self.partner.with_context(show_email=True).name_get()[0][1]
        self.assertEqual(
            email_get, self.partner.name + ' <' + self.partner.email + '>')

    def test_res_partner_show_email_only(self):
        address_get = self.partner.with_context(
            show_address_only=True).name_get()[0][1]
        address = address_get.split("\n")[1:]
        self.assertEqual(address[1], self.partner.country_id.name)
