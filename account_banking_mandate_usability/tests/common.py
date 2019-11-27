# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class AccountBankingMandateUsabilityCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(AccountBankingMandateUsabilityCommon, cls).setUpClass()
        cls.bank_model = cls.env['res.partner.bank']
        account_iban = 'ES9501821115461112689452'
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })
        cls.bank = cls.bank_model.create({
            'acc_number': account_iban,
            'partner_id': cls.partner.id,
        })

