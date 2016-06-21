# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestSaleCrmLeadLink(common.TransactionCase):

    def setUp(self):
        super(TestSaleCrmLeadLink, self).setUp()
        self.opportunity = self.env.ref('crm.crm_case_14')

    def test_convert_to_sale(self):
        wiz_create = self.env['crm.make.sale'].create(
            {'partner_id': self.opportunity.partner_id.id})
        value = wiz_create.with_context(active_ids=[self.opportunity.id]
                                        ).makeOrder()
        for sale in self.env['sale.order'].browse(value.get('res_id', [])):
            self.assertEqual(sale.lead_id.id, self.opportunity.id,
                             'Lead not correctly set.')

    def test_sale_order_lines(self):
        sale = self.env.ref('sale.sale_order_1')
        sale.lead_id = self.opportunity.id
        for line in sale.order_line:
            self.assertTrue((line.id in self.opportunity.sale_lines.ids),
                            'Sale lines are not correctly set.')
