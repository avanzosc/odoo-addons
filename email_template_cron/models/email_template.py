# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging
import pytz
from openerp import api, fields, models
from openerp.addons.base.ir.ir_cron import _intervalTypes

_logger = logging.getLogger(__name__)
context_timestamp = fields.Datetime.context_timestamp
str2datetime = fields.Datetime.from_string


class EmailTemplate(models.Model):
    _inherit = 'email.template'

    @api.model
    def _get_selection_interval_type(self):
        return self.env['ir.cron'].fields_get(
            allfields=['interval_type'])['interval_type']['selection']

    def default_interval_type(self):
        default_dict = self.env['ir.cron'].default_get(['interval_type'])
        return default_dict.get('interval_type')

    cron_active = fields.Boolean(string='Active [Cron]', default=False)
    interval_number = fields.Integer(
        string='Interval Number', help="Repeat every x.")
    interval_type = fields.Selection(
        selection='_get_selection_interval_type', string='Interval Unit',
        required=True, default=default_interval_type)
    nextcall = fields.Datetime(
        string='Next Execution Date', required=True,
        help="Next planned execution date for this job.",
        default=fields.Datetime.now())
    cron_domain = fields.Char(string='Domain', default="[]")

    @api.model
    def process_automatic_tmpl_queue(self):
        message_obj = self.env['mail.compose.message']
        try:
            for template in self.search([
                    ('cron_active', '=', True),
                    ('nextcall', '<=', fields.Datetime.now())]):
                now = context_timestamp(
                    template, str2datetime(fields.Datetime.now()))
                nextcall = context_timestamp(
                    template, str2datetime(template.nextcall))
                if nextcall < now:
                    update_dict = message_obj.onchange_template_id(
                        template_id=template.id, composition_mode='mass_mail',
                        model=template.model_id.model, res_id=None)
                    wiz = message_obj.with_context(
                        default_template_id=template.id,
                        default_composition_mode='mass_mail',
                        active_model=template.model_id.model,
                        active_domain=eval(template.cron_domain)).create(
                        update_dict.get('value', {}))
                    wiz.send_mail()
                    nextcall += _intervalTypes[template.interval_type](
                        template.interval_number)
                template.nextcall = nextcall.astimezone(pytz.UTC)
        except Exception:
            _logger.exception("Failed processing mail queue")
        return True
