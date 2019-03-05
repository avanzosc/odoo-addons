# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase


class ContactsSchoolTest(TransactionCase):

    def setUp(self):
        super(ContactsSchoolTest, self).setUp()
        self.partner_model = self.env['res.partner']
        self.partner1 = self.env.ref('base.res_partner_address_1')
        self.partner2 = self.env.ref('base.res_partner_address_2')
        self.partner1.educational_category = 'federation'
        self.partner1.educational_category = 'association'

    def test_contacts_scholl(self):
        partner_vals = {'name': 'Partner for test contacts_school',
                        'educational_category': 'family',
                        'assoc_fede_ids':
                        [(0, 0, {'partner_id': self.partner1.id}),
                         (0, 0, {'partner_id': self.partner2.id})]}
        partner = self.partner_model.create(partner_vals)
        self.assertEqual(partner.family, 'FAM-00001')
