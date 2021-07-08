
from odoo import api, models, fields


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    error_bank_acc = fields.Boolean(
        string='Bank account error',
        compute="_compute_validate_bank_account")

    @api.depends('acc_type')
    def _compute_validate_bank_account(self):
        for record in self:
            record.error_bank_acc = False
            if record.acc_type not in 'iban':
                record.error_bank_acc = True

    def create_validate_bank_account_mandate(self):
        wiz_obj = self.sudo().env["res.partner.bank.mandate.generator"]
        mandate_wiz = wiz_obj.create({
            "bank_ids": [self.id],
            "mandate_format": "sepa",
            "mandate_type": "recurrent",
            "mandate_scheme": "CORE",
            "mandate_recurrent_sequence_type": "recurring",
            "signed": True,
            "validate": True,
        })
        mandate_wiz.button_generate_mandates()
