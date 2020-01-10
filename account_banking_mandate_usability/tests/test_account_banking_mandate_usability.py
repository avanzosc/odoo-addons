# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import AccountBankingMandateUsabilityCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestAccountBankingMandateUsability(AccountBankingMandateUsabilityCommon):

    def test_generate_banking_mandate_wizard(self):
        mandate_field_list = self.mandate_model.fields_get_keys()
        wizard_field_list = self.mandate_wiz_model.fields_get_keys()
        mandate_dict = self.mandate_model.default_get(mandate_field_list)
        wizard_dict = self.mandate_wiz_model.with_context(
            active_model=self.bank_model._name,
            active_ids=self.bank.ids).default_get(wizard_field_list)
        self.assertEquals(wizard_dict.get("bank_ids"), self.bank.ids)
        self.assertEquals(
            wizard_dict.get("mandate_format"),
            mandate_dict.get("format", False))
        self.assertEquals(
            wizard_dict.get("mandate_type"),
            mandate_dict.get("type", False))
        self.assertEquals(
            wizard_dict.get("mandate_scheme"),
            mandate_dict.get("scheme", False))
        self.assertEquals(
            wizard_dict.get("mandate_recurrent_sequence_type"),
            mandate_dict.get("recurrent_sequence_type", False))
        mandate_selection = self.mandate_model.fields_get(
            allfields=mandate_field_list)
        mandate_format_sel = self.mandate_wiz_model._get_format_selection()
        self.assertEquals(
            mandate_selection["format"]["selection"], mandate_format_sel)
        mandate_type_sel = self.mandate_wiz_model._get_type_selection()
        self.assertEquals(
            mandate_selection["type"]["selection"], mandate_type_sel)
        mandate_scheme_sel = self.mandate_wiz_model._get_scheme_selection()
        self.assertEquals(
            mandate_selection["scheme"]["selection"], mandate_scheme_sel)
        mandate_recurrent_sequence_type_sel = (
            self.mandate_wiz_model._get_recurrent_sequence_type_selection())
        self.assertEquals(
            mandate_selection["recurrent_sequence_type"]["selection"],
            mandate_recurrent_sequence_type_sel)
