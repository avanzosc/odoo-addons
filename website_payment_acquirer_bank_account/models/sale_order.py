from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    bank_account_id = fields.Many2one(
        "res.bank.account",
        string="Bank Account",
        help="Bank account selected for the payment.",
    )

    def confirm_order(self):
        self.ensure_one()
        if self.bank_account_id:
            # Si hay una cuenta bancaria seleccionada
            self.payment_mode_id = self.bank_account_id.payment_method_id
            # Crear la cuenta bancaria si es nueva
            if not self.bank_account_id.exists():
                self.env["res.bank.account"].create(
                    {
                        "name": self.bank_account_id.name,
                        "bank_account": self.bank_account_id.bank_account,
                        "partner_id": self.partner_id.id,
                    }
                )
        else:
            raise ValidationError(_("Please select a bank account."))
