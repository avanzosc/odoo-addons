
from odoo import _, api, fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    signature_driver = fields.Binary('Signature Driver', help='Signature received through the portal.', copy=False, attachment=True, max_width=1024, max_height=1024)
    date_signature_driver = fields.Date('Date signature driver')
    signature_farm = fields.Binary('Signature Farm', help='Signature received through the portal.', copy=False, attachment=True, max_width=1024, max_height=1024)
    date_signature_farm = fields.Date('Date signature farm')

    def _get_report_base_filename(self):
        self.ensure_one()
        fname = "Saca Form-%s" % self.name
        return fname

    def has_to_be_signed(self, sign_by=None):
        if sign_by == 'farm':
            return not self.signature_farm
        if sign_by == 'driver':
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
        mail_template = self.env.ref('website_custom_saca.saca_pdf_send')
        mail_template.send_mail(self.id, force_send=True)
