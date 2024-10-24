from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)

class MailingTrace(models.Model):
    _inherit = "mailing.trace"

    mail_message_id = fields.Many2one(
        "mail.message",
        string="Chatter Message",
        help="The chatter message related to this email trace.",
    )

    mail_message_id_int = fields.Integer(
        string="Chatter ID (tech)",
        help="ID of the related mail_message. This field is an integer field because "
        "the related mail_message can be deleted separately from its statistics. "
        "However the ID is needed for several action and controllers.",
        index=True,
    )

    email = fields.Char(string="Email", required=True)
    message_id = fields.Char(string="Message ID", required=True)
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("tracking_added", "Tracking Added"),
            ("sent", "Sent"),
        ],
        string="Status",
        default="draft",
    )

    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            if "mail_message_id" in values:
                values["mail_message_id_int"] = values["mail_message_id"]
        return super(MailingTrace, self).create(values_list)

    def _get_records(self, mail_mail_ids=None, mail_message_ids=None, domain=None):
        base_domain = []
        if not self.ids and mail_mail_ids:
            base_domain = [("mail_mail_id_int", "in", mail_mail_ids)]
        elif not self.ids and mail_message_ids:
            base_domain = [("mail_message_id_int", "in", mail_message_ids)]
        else:
            base_domain = [("id", "in", self.ids)]

        if domain:
            base_domain = ["&"] + domain + base_domain

        return self.search(base_domain)

    @api.model
    def get_chatter_id(self, model_name, record_id):
        """
        Devuelve el Chatter Message ID y los Mailing Trace IDs para el modelo y registro dados.
        """
        _logger.info("Getting Chatter Message ID for model: %s, record ID: %s", model_name, record_id)

        record_id = int(record_id)
        if not record_id:
            _logger.warning("Record ID is not an integer: %s", record_id)
            return {'chatter_message_id': None, 'mailing_trace_ids': []}

        record = self.env[model_name].sudo().browse(record_id)

        if record.exists():
            _logger.info("Record found: %s", record)

            chatter_messages = self.env['mail.message'].search([
                ('res_id', '=', record_id),
                ('model', '=', model_name)
            ])

            # Inicializar los valores de retorno
            chatter_message_id = None
            mailing_trace_ids = []

            if chatter_messages:
                chatter_message_id = chatter_messages[0].id
                _logger.info("Chatter Message ID found: %s", chatter_message_id)

            # Verificar si el modelo tiene el atributo mailing_trace_ids
            if hasattr(chatter_messages, 'mailing_trace_ids'):
                mailing_trace_ids = chatter_messages.mailing_trace_ids.ids  # Suponiendo que hay una relación One2many

                if not mailing_trace_ids:
                    _logger.warning("No Mailing Trace IDs found for record ID: %s in model: %s", record_id, model_name)
            else:
                _logger.warning("The model %s does not have mailing_trace_ids attribute", model_name)

            return {
                'chatter_message_id': chatter_message_id,
                'mailing_trace_ids': mailing_trace_ids,
            }
        else:
            _logger.warning("Record not found for model: %s, ID: %s", model_name, record_id)
            return {'chatter_message_id': None, 'mailing_trace_ids': []}
