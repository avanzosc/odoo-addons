# -*- coding: utf-8 -*-
# Copyright © 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestL10nEsAeatMod347Ext(common.TransactionCase):

    def setUp(self):
        super(TestL10nEsAeatMod347Ext, self).setUp()
        self.report_obj = self.env['l10n.es.aeat.mod347.report']
        self.partner = self.env.ref('base.res_partner_9')
        fiscal_year = self.env['account.fiscalyear'].search([], limit=1)
        report_vals = {'company_vat': 'B20875340',
                       'fiscalyear_id': fiscal_year.id,
                       'period_type': '0A',
                       'support_type': 'T',
                       'contact_phone': '943999888'}
        self.report = self.report_obj.create(report_vals)
        self.report.onchange_period_type()
        self.env['l10n.es.aeat.mod347.partner_record'].create(
            {'partner_id': self.partner.id,
             'report_id': self.report.id})

    def test_l10n_es_aeat_mod_347_ext(self):
        self.report.button_calculate()
        self.assertEqual(
            self.report.partner_record_ids[0].state, 'pending')
        self.report.button_mass_mailing()
        self.assertEqual(
            self.report.partner_record_ids[0].state, 'sent')
        self.report.button_mass_mailing_unanswered()
        self.assertEqual(
            self.partner.num_347_records, 1)
        res = self.partner.show_partner_347_records()
        cond = [('partner_id', '=', self.partner.id)]
        self.assertEqual(res.get('domain'), cond)
