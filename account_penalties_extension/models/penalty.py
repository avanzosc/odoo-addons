# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountPenalty(models.Model):
    _inherit = "account.penalty"

    penalty_price = fields.Float(
        string="Penalty Price",
        digits="Product Price",
        help="Base price from the product. Can be edited manually.",
    )

    @api.onchange("penalty_type_id")
    def _onchange_penalty_type_set_price(self):
        """
        Al cambiar el tipo, busca el precio del producto relacionado
        y rellena el precio base y el importe final.
        """
        if self.penalty_type_id and self.penalty_type_id.product_id:
            price = self.penalty_type_id.product_id.list_price
            self.penalty_price = price
            self.amount = price

    @api.onchange("penalty_price")
    def _onchange_penalty_price_update_amount(self):
        """
        Si el usuario edita el 'Penalty Price' a mano,
        actualizamos el 'Amount' para que la factura salga correcta.
        """
        self.amount = self.penalty_price
