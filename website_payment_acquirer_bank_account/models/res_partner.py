from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    bank_account_ids = fields.One2many(
        "res.bank.account",
        "partner_id",
        string="Bank Accounts",
    )
