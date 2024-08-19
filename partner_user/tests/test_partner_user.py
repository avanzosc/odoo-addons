# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests.common import SavepointCase


class TestPartnerUser(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerUser, cls).setUpClass()
        cls.wizard = cls.env['create.user.wizard']
        cls.company = cls.env.ref('base.res_partner_1')
        cls.contact = cls.env.ref('base.res_partner_address_1')

    def test_partner_user_company(self):
        self.assertNotEqual(
            len(self.company.child_ids.filtered(lambda p: p.email)),
            len(self.company.child_ids))
        self.assertEqual(len(self.company.mapped('child_ids.user_ids')), 0)
        wizard = self.wizard.create(
            self.wizard.with_context(active_ids=self.company.ids).default_get(
                ['line_ids']))
        self.assertTrue(len(wizard.line_ids), len(self.company.child_ids))
        line_no_email = wizard.line_ids.filtered(lambda l: not l.email)[:1]
        line_no_email.write({
            'email': 'test@test.com',
        })
        self.assertNotEquals(
            line_no_email.email, line_no_email.partner_id.email)
        wizard.action_apply()
        self.assertNotEqual(len(self.company.mapped('child_ids.user_ids')), 0)
        self.assertEquals(
            line_no_email.email, line_no_email.partner_id.email)

    def test_partner_user_contact(self):
        self.assertTrue(self.contact.email)
        self.assertEqual(len(self.contact.user_ids), 0)
        wizard = self.wizard.create(
            self.wizard.with_context(active_ids=self.contact.ids).default_get(
                ['line_ids']))
        self.assertEqual(len(wizard.line_ids), 1)
        wizard.action_apply()
        self.assertNotEqual(len(self.contact.user_ids), 0)
