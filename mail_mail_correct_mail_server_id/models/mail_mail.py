from odoo import models, api

class MailMail(models.Model):
    _inherit = "mail.mail"

    @api.model
    def create(self, vals):
        mail = super().create(vals)
        if mail.company_id:
            mail_server = self.env['ir.mail_server'].search([
                ('company_id', '=', mail.company_id.id)
            ], limit=1)
            if mail_server:
                mail.mail_server_id = mail_server.id
        return mail
