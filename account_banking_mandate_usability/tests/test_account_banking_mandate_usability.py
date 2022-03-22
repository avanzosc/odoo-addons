# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests import tagged

from .common import AccountBankingMandateUsabilityCommon


@tagged("post_install", "-at_install")
class TestAccountBankingMandateUsability(AccountBankingMandateUsabilityCommon):
    def test_generate_banking_mandate_wizard_defaults(self):
        mandate_field_list = self.mandate_model.fields_get_keys()
        mandate_dict = self.mandate_model.default_get(mandate_field_list)
        self.assertEqual(self.wizard_dict.get("bank_ids"), [(6, 0, self.bank.ids)])
        self.assertEqual(
            self.wizard_dict.get("mandate_format"), mandate_dict.get("format", False)
        )
        self.assertEqual(
            self.wizard_dict.get("mandate_type"), mandate_dict.get("type", False)
        )
        self.assertEqual(
            self.wizard_dict.get("mandate_scheme"), mandate_dict.get("scheme", False)
        )
        self.assertEqual(
            self.wizard_dict.get("mandate_recurrent_sequence_type"),
            mandate_dict.get("recurrent_sequence_type", False),
        )
        mandate_selection = self.mandate_model.fields_get(allfields=mandate_field_list)
        mandate_format_sel = self.mandate_wiz_model._get_format_selection()
        self.assertEqual(mandate_selection["format"]["selection"], mandate_format_sel)
        mandate_type_sel = self.mandate_wiz_model._get_type_selection()
        self.assertEqual(mandate_selection["type"]["selection"], mandate_type_sel)
        mandate_scheme_sel = self.mandate_wiz_model._get_scheme_selection()
        self.assertEqual(mandate_selection["scheme"]["selection"], mandate_scheme_sel)
        mandate_recurrent_sequence_type_sel = (
            self.mandate_wiz_model._get_recurrent_sequence_type_selection()
        )
        self.assertEqual(
            mandate_selection["recurrent_sequence_type"]["selection"],
            mandate_recurrent_sequence_type_sel,
        )

    def test_generate_banking_mandate_wizard_onchanges(self):
        self.assertFalse(self.wizard.signed)
        self.assertFalse(self.wizard.validate)
        self.wizard.validate = True
        self.wizard._onchange_validate()
        self.assertTrue(self.wizard.signed)
        self.assertTrue(self.wizard.validate)
        self.wizard.signed = False
        self.wizard._onchange_signed()
        self.assertFalse(self.wizard.signed)
        self.assertFalse(self.wizard.validate)

    def test_generate_banking_mandate_wizard(self):
        today = fields.Date.context_today(self.mandate_model)
        self.assertFalse(self.bank._check_active_mandate())
        self.assertIn(self.bank, self.wizard.bank_ids)
        self.wizard.write(
            {
                "signed": True,
                "validate": True,
            }
        )
        self.wizard.button_generate_mandates()
        self.assertTrue(self.bank._check_active_mandate())
        mandate = self.bank.mandate_ids[:1]
        self.assertEqual(mandate.signature_date, today)
        self.assertTrue(mandate.state, "valid")

    def test_generate_banking_mandate_wizard_force_company(self):
        bank = self.bank.with_company(self.env.user.company_id.id)
        wizard = self.wizard.with_company(self.env.user.company_id.id)
        today = fields.Date.context_today(self.mandate_model)
        self.assertFalse(bank._check_active_mandate())
        self.assertIn(bank, wizard.bank_ids)
        wizard.write(
            {
                "signed": True,
                "validate": True,
            }
        )
        wizard.button_generate_mandates()
        self.assertTrue(bank._check_active_mandate())
        mandate = bank.mandate_ids[:1]
        self.assertEqual(mandate.signature_date, today)
        self.assertTrue(mandate.state, "valid")
