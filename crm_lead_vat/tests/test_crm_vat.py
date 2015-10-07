# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import exceptions
from openerp.tests import common


class TestCrmVat(common.TransactionCase):

    def setUp(self):
        super(TestCrmVat, self).setUp()
        self.crm_lead_model = self.env['crm.lead']
        self.partner1 = self.env.ref('base.res_partner_1')
        self.crm_lead_partner_ok = self.crm_lead_model.create(
            {'name': 'Test',
             'vat': 'ATU00000024',
             })
        self.crm_lead_partner_wrong = self.crm_lead_model.create(
            {'name': 'Test - 0',
             'vat': 'ESU00000024',
             })
        self.crm_lead_no_country = self.crm_lead_model.create(
            {'name': 'Test - 1',
             'vat': 'U00000024',
             })
        self.crm_lead_wrong_country = self.crm_lead_model.create(
            {'name': 'Test - 2',
             'vat': 'AAU00000024',
             })
        self.lead = self.crm_lead_model.create(
            {'name': 'Test - 3'})

    def test_ok_crm_vat(self):
        self.assertTrue(self.crm_lead_model._lead_create_contact(
            self.crm_lead_partner_ok,
            self.crm_lead_partner_ok.name, False, False))

    def test_wrong_crm_vat(self):
        with self.assertRaises(exceptions.ValidationError):
            self.crm_lead_model._lead_create_contact(
                self.crm_lead_partner_wrong,
                self.crm_lead_partner_wrong.name, False, False)

    def test_wrong_no_country(self):
        with self.assertRaises(exceptions.ValidationError):
            self.crm_lead_model._lead_create_contact(
                self.crm_lead_no_country,
                self.crm_lead_no_country.name, False, False)

    def test_wrong_country(self):
        with self.assertRaises(exceptions.ValidationError):
            self.crm_lead_model._lead_create_contact(
                self.crm_lead_wrong_country,
                self.crm_lead_wrong_country.name, False, False)

    def test_onchange_partner_id(self):
        """Lead gets VAT from partner when linked to it."""
        self.partner1.vat = 'ATU00000024'
        result = self.lead.on_change_partner_id(self.partner1.id)
        self.lead.vat = result['value']['vat']
        self.assertEqual(self.partner1.vat, self.lead.vat)
