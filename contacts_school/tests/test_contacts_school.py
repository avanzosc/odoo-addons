# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestContactsSchool(TransactionCase):

    def setUp(self):
        super(TestContactsSchool, self).setUp()
        self.family_sequence = self.env.ref(
            'contacts_school.seq_res_partner_family')
        self.partner_model = self.env['res.partner']
        self.family_model = self.env['res.partner.family']
        self.partner1 = self.env.ref('base.res_partner_address_1')
        self.partner2 = self.env.ref('base.res_partner_address_2')
        self.partner1.educational_category = 'federation'
        self.partner1.educational_category = 'association'
        self.partner_bank = self.env['res.partner.bank'].search([], limit=1)

    def test_contacts_school(self):
        partner_vals = {
            'name': 'Partner for test contacts_school',
            'educational_category': 'family',
            'assoc_fede_ids':
                [(0, 0, {'partner_id': self.partner1.id}),
                 (0, 0, {'partner_id': self.partner2.id})]}
        code = self._get_next_code()
        partner = self.partner_model.create(partner_vals)
        self.assertEqual(partner.family, code)
        partner_vals = {
            'name': 'student for test contacts_school',
            'educational_category': 'student',
        }
        student = self.partner_model.create(partner_vals)
        student.family_ids = [(0, 0, {
            'child2_id': student.id,
            'responsible_id': 1})]

    def _get_next_code(self):
        return self.family_sequence.get_next_char(
            self.family_sequence.number_next_actual
        )
