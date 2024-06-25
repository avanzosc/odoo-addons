import pytz

from odoo import fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    signature_driver = fields.Image(
        string="Driver's Signature",
        help="Signature received through the portal.",
        copy=False,
        attachment=True,
        max_width=1024,
        max_height=1024,
    )
    date_signature_driver = fields.Date("Date signature driver")
    signature_farm = fields.Image(
        string="Farm's Signature Farm",
        help="Signature received through the portal.",
        copy=False,
        attachment=True,
        max_width=1024,
        max_height=1024,
    )
    date_signature_farm = fields.Date("Date signature farm")

    ticket_farm_attachment_id = fields.Many2one(
        string="Farm ticket attachment",
        comodel_name="ir.attachment",
    )
    ticket_slaughterhouse_attachment_id = fields.Many2one(
        string="Slaughterhouse ticket attachment",
        comodel_name="ir.attachment",
    )

    def _get_report_base_filename(self):
        self.ensure_one()
        fname = "Saca Form-%s" % self.name
        return fname

    def has_to_be_signed(self, sign_by=None):
        if sign_by == "farm":
            return not self.signature_farm
        if sign_by == "driver":
            return not self.signature_driver
        return not self.signature_driver and not self.signature_farm

    def clear_signature_farm(self):
        self.ensure_one()
        self.signature_farm = None
        self.date_signature_farm = None

    def clear_signature_driver(self):
        self.ensure_one()
        self.signature_driver = None
        self.date_signature_driver = None

    def action_send_saca_mail(self):
        mail_template = self.env.ref("website_custom_saca.saca_pdf_send")
        mail_template.send_mail(self.id, force_send=True)

    def set_timesheet_start_stop(self, stamp_type, timesheet_id):
        self.ensure_one()
        timezone = pytz.timezone(self._context.get("tz") or "UTC")
        timesheet = self.timesheet_ids.filtered(lambda t: t.id == timesheet_id)
        now = (
            fields.Datetime.now()
            .replace(tzinfo=pytz.timezone("UTC"))
            .astimezone(timezone)
            .time()
        )
        now = now.strftime("%H:%M:%S")
        if stamp_type == "btn_start":
            timesheet.time_start = self.conv_time_float(now)
        else:
            timesheet.time_stop = self.conv_time_float(now)

    def conv_time_float(self, value):
        vals = value.split(":")
        t, hours = divmod(float(vals[0]), 24)
        t, minutes = divmod(float(vals[1]), 60)
        minutes = minutes / 60.0
        return hours + minutes
