# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo.tests import common


class TestPurchaseContractSpecification(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPurchaseContractSpecification, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner to test',
        })
        cls.purchase_order = cls.env['purchase.order'].create({
            'partner_id': cls.partner.id,
        })
        cls.template1 = cls.env['contract.condition.template'].create({
            'name': 'Warranties',
        })
        cls.condition1 = cls.env['contract.condition'].create({
            'name': 'Warranty',
            'description': 'Products are guarantee by manufacturer',
            'template_ids': [(4, cls.template1.id)],
        })
        cls.template2 = cls.env['contract.condition.template'].create({
            'name': 'Warranties',
        })
        cls.condition2 = cls.env['contract.condition'].create({
            'name': 'Warranty',
            'description': 'Products are guarantee by manufacturer',
            'template_ids': [(4, cls.template2.id)],
        })

    def test_import(self):
        self.assertFalse(self.purchase_order.condition_ids)
        self.assertFalse(self.purchase_order.condition_tmpl_id)
        self.purchase_order.condition_tmpl_id = self.template1
        self.assertFalse(self.purchase_order.condition_ids)
        self.purchase_order._onchange_condition_tmpl_id()
        self.assertTrue(self.purchase_order.condition_ids)
        self.assertEqual(len(self.purchase_order.condition_ids),
                         len(self.template1.condition_ids))
        self.purchase_order.condition_tmpl_id = self.template2
        self.purchase_order._onchange_condition_tmpl_id()
        self.assertEqual(len(self.purchase_order.condition_ids),
                         (2 * len(self.template1.condition_ids)) +
                         len(self.template2.condition_ids))
