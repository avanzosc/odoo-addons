from odoo import _, fields, models
from odoo.exceptions import ValidationError




class ResBankAccount(models.Model):
    _name = "res.bank.account"
    _description = "Bank Account"

    name = fields.Char(string="Account Name", required=True)
    bank_account = fields.Char(string="Bank Account", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
