# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class L10nEsAeatMod347Report(models.Model):
    _inherit = 'l10n.es.aeat.mod347.report'

    @api.multi
    def button_mass_mailing(self):
        partner_records = self.partner_record_ids.filtered(
            lambda x: x.state == 'pending' and x.partner_id.email)
        self._send_email_from_button(partner_records)

    @api.multi
    def button_mass_mailing_unanswered(self):
        partner_records = self.partner_record_ids.filtered(
            lambda x: x.state == 'sent' and x.partner_id.email)
        self._send_email_from_button(partner_records)

    @api.multi
    def _send_email_from_button(self, partners_347):
        template = self.env.ref(
            'l10n_es_aeat_mod347_ext.email_template_mod347_partner_record',
            False)
        for partner_347 in partners_347:
            if partner_347.partner_id.notify_email != 'always':
                partner_347.partner_id.notify_email = 'always'
            vals = {'email_from': template.email_from,
                    'subject': template.subject,
                    'reply_to': template.reply_to,
                    'body': template.body_html,
                    'partner_ids': [(6, 0, [partner_347.partner_id.id])]}
            wizard = self.env['mail.compose.message'].with_context(
                default_composition_mode='mass_mail',
                default_template_id=template.id,
                default_use_template=True,
                default_no_auto_thread=True,
                active_domain=[['id', '=', partner_347.id]],
                active_id=partner_347.id,
                active_ids=partner_347.ids,
                active_model='l10n.es.aeat.mod347.partner_record',
                default_model='l10n.es.aeat.mod347.partner_record',
                default_res_id=partner_347.id,
            ).create(vals)
            wizard.send_mail()


class L10nEsAeatMod347Partner_record(models.Model):
    _name = 'l10n.es.aeat.mod347.partner_record'
    _inherit = ['l10n.es.aeat.mod347.partner_record', 'mail.thread']

    @api.multi
    def _compute_state(self):
        for partner_record in self:
            state = 'pending'
            found = partner_record.mapped('message_ids').filtered(
                lambda x: x.subject and '347' in x.subject)
            if found:
                found = partner_record.mapped('message_ids').filtered(
                    lambda x: partner_record.partner_id.email in x.email_from)
                state = 'contested' if found else 'sent'
            partner_record.state = state

    company_id = fields.Many2one(
        related='report_id.company_id', store=True)
    fiscalyear_id = fields.Many2one(
        related='report_id.fiscalyear_id', store=True)
    report_identifier = fields.Char(
        related='report_id.name', store=True)
    company_vat = fields.Char(
        related='report_id.company_vat', store=True)
    period_type = fields.Selection(
        related='report_id.period_type', store=True)
    state = fields.Selection(
        selection=[('pending', 'Pending shipment email'),
                   ('sent', 'Email sent'),
                   ('contested', 'Contested')], string="State",
        compute='_compute_state')
