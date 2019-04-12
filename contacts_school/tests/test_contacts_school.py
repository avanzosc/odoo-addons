# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestContactsSchool(TransactionCase):

    def setUp(self):
        super(TestContactsSchool, self).setUp()
        self.partner_model = self.env['res.partner']
        self.payer_model = self.env['res.partner.student.payer']
        self.family_model = self.env['res.partner.family']
        self.partner1 = self.env.ref('base.res_partner_address_1')
        self.partner2 = self.env.ref('base.res_partner_address_2')
        self.partner1.educational_category = 'federation'
        self.partner1.educational_category = 'association'
        self.partner_bank = self.env['res.partner.bank'].search([], limit=1)

    def test_contacts_scholl(self):
        partner_vals = {'name': 'Partner for test contacts_school',
                        'educational_category': 'family',
                        'assoc_fede_ids':
                        [(0, 0, {'partner_id': self.partner1.id}),
                         (0, 0, {'partner_id': self.partner2.id})]}
        partner = self.partner_model.create(partner_vals)
        self.assertEqual(partner.family, 'FAM-00001')
        partner_vals = {'name': 'student for test contacts_school',
                        'educational_category': 'student'}
        student = self.partner_model.create(partner_vals)
        payer_vals = {'student_id': student.id,
                      'partner_id': self.partner_bank.partner_id.id,
                      'percentage': 200}
        payer = self.payer_model.create(payer_vals)
        with self.assertRaises(ValidationError):
            student._check_payer_percentage()
        student.family_ids = [(0, 0, {'child2_id': student.id,
                                      'responsible_id': 1})]
        payer.onchange_student_id()
        self.assertEqual(payer.allowed_family_ids[0].id, 1)
        payer.onchange_partner_id()
        self.assertEqual(payer.bank_id, self.partner_bank)
