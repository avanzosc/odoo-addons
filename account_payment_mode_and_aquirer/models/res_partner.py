from odoo import _, fields, models
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"

    bank_account_ids = fields.One2many(
        "res.bank.account",
        "partner_id",
        string="Bank Accounts",
    )
