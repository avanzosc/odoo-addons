# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class AccountBankingMandateUsabilityCommon(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(AccountBankingMandateUsabilityCommon, cls).setUpClass()
        cls.bank_model = cls.env["res.partner.bank"]
        cls.mandate_model = cls.env["account.banking.mandate"]
        cls.mandate_wiz_model = cls.env["res.partner.bank.mandate.generator"]
        account_iban = "ES9501821115461112689452"
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.bank = cls.bank_model.create(
            {
                "acc_number": account_iban,
                "partner_id": cls.partner.id,
            }
        )
        cls.mandate_wiz_model = cls.env[
            "res.partner.bank.mandate.generator"
        ].with_context(active_model=cls.bank_model._name, active_ids=cls.bank.ids)
        wizard_field_list = cls.mandate_wiz_model.fields_get_keys()
        cls.wizard_dict = cls.mandate_wiz_model.default_get(wizard_field_list)
        cls.wizard = cls.mandate_wiz_model.create(cls.wizard_dict)
