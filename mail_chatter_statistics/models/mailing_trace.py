import logging

from odoo import api, fields, models

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
        "However, the ID is needed for several actions and controllers.",
        index=True,
    )

    email = fields.Char(string="Email")
    message_id = fields.Char(string="Message ID")

    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("tracking_added", "Tracking Added"),
            ("sent", "Sent"),
            ("clicked", "Clicked"),
            ("opened", "Opened"),
            ("bounced", "Bounced"),
            ("replied", "Replied"),
        ],
        string="Status",
        default="draft",
    )

    sent_at = fields.Datetime(string="Sent At")
    clicked_at = fields.Datetime(string="Clicked At")
    opened_at = fields.Datetime(string="Opened At")
    bounced_at = fields.Datetime(string="Bounced At", computed="_compute_bounced_at")
    replied_at = fields.Datetime(string="Replied At")
    user_agent = fields.Char(string="User Agent")

    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            if "mail_message_id" in values:
                values["mail_message_id_int"] = values["mail_message_id"]
        return super(MailingTrace, self).create(values_list)

    def _get_records(self, mail_mail_ids=None, mail_message_ids=None, domain=None):
        base_domain = []
        if not self.ids and mail_mail_ids:
            base_domain = [("mail_message_id_int", "in", mail_mail_ids)]
        elif not self.ids and mail_message_ids:
            base_domain = [("mail_message_id_int", "in", mail_message_ids)]
        else:
            base_domain = [("id", "in", self.ids)]

        if domain:
            base_domain = ["&"] + domain + base_domain

        return self.search(base_domain)

    @api.model
    def get_chatter_id(self, model_name, record_id):
        _logger.info(
            "Getting Chatter Message ID for model: %s, record ID: %s",
            model_name,
            record_id,
        )

        record_id = int(record_id)
        if not record_id:
            _logger.warning("Record ID is not an integer: %s", record_id)
            return {"chatter_message_id": None, "mailing_trace_ids": []}

        record = self.env[model_name].sudo().browse(record_id)

        if record.exists():
            _logger.info("Record found: %s", record)

            chatter_messages = self.env["mail.message"].search(
                [("res_id", "=", record_id), ("model", "=", model_name)]
            )
            message_trace_mapping = {}

            for message in chatter_messages:
                mailing_trace_ids = message.mailing_trace_ids.ids
                message_trace_mapping[message.id] = mailing_trace_ids

                if not mailing_trace_ids:
                    _logger.warning(
                        "No Mailing Trace IDs found for Chatter Message ID: %s",
                        message.id,
                    )

            return message_trace_mapping
        else:
            _logger.warning(
                "Record not found for model: %s, ID: %s", model_name, record_id
            )
            return {"chatter_message_id": None, "mailing_trace_ids": []}

    def track_open(self):
        self.status = "opened"
        self.opened_at = fields.Datetime.now()

    def track_click(self):
        self.status = "clicked"
        self.clicked_at = fields.Datetime.now()

    @api.depends("mail_message_id.mail_notification_ids.notification_status")
    def _compute_bounced_at(self):
        for record in self:
            notifications = record.mail_message_id.mail_notification_ids.sorted(
                key=lambda n: n.create_date, reverse=True
            )
            if notifications and notifications[0].notification_status == "bounced":
                record.bounced_at = fields.Datetime.now()
            else:
                record.bounced_at = False

    def track_reply(self):
        self.status = "replied"
        self.replied_at = fields.Datetime.now()

    @api.model
    def default_get(self, fields):
        res = super(MailingTrace, self).default_get(fields)
        res.update(
            {
                "sent_at": self.replied,
                "clicked_at": self.clicked,
                "opened_at": self.opened,
                "bounced_at": self.bounced,
                "replied_at": self.replied,
            }
        )
        return res

    @api.onchange("replied", "clicked", "opened", "bounced", "invoiced")
    def _onchange_dates(self):
        self.sent_at = self.replied
        self.clicked_at = self.clicked
        self.opened_at = self.opened
        self.bounced_at = self.bounced
        self.replied_at = self.replied

    def set_opened(self, mail_mail_ids=None, mail_message_ids=None):
        super(MailingTrace, self).set_opened(mail_mail_ids, mail_message_ids)
        if mail_message_ids:
            self.mail_message_id = mail_message_ids[0]

    def set_clicked(self, mail_mail_ids=None, mail_message_ids=None):
        super(MailingTrace, self).set_clicked(mail_mail_ids, mail_message_ids)
        if mail_message_ids:
            self.mail_message_id = mail_message_ids[0]

    def set_replied(self, mail_mail_ids=None, mail_message_ids=None):
        super(MailingTrace, self).set_replied(mail_mail_ids, mail_message_ids)
        if mail_message_ids:
            self.mail_message_id = mail_message_ids[0]

    def set_bounced(self, mail_mail_ids=None, mail_message_ids=None):
        super(MailingTrace, self).set_bounced(mail_mail_ids, mail_message_ids)
        if mail_message_ids:
            self.mail_message_id = mail_message_ids[0]
