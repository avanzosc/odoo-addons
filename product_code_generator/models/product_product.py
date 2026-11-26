# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        for product, vals in zip(products, vals_list, strict=False):
            if "barcode" not in vals:
                product.barcode = product._generate_ean13_barcode()
        return products

    def generate_code(self):
        product_code = self.env["product.code"]
        for product in self:
            if not product.default_code:
                prefix = product_code._build_prefix(
                    product.product_brand_id,
                    product.family_id,
                    product.sub_family_id,
                    product.season_id,
                )
                code = product_code.search([("name", "=", prefix)], limit=1)
                if not code:
                    code = product_code.create(
                        {
                            "brand_id": product.product_brand_id.id,
                            "family_id": product.family_id.id,
                            "sub_family_id": product.sub_family_id.id,
                            "season_id": product.season_id.id,
                        }
                    )
                product.default_code = code.sequence_id.next_by_id()
            if not product.barcode:
                product.barcode = product._generate_ean13_barcode()

    def _generate_ean13_barcode(self):
        self.ensure_one()
        company = self.company_id or self.env.company
        if not company.barcode_prefix:
            raise UserError(
                _(
                    "Set a barcode prefix on the company before generating "
                    "product barcodes."
                )
            )
        sequence_number = self._get_barcode_sequence(company).next_by_id()
        ean12 = str(company.barcode_prefix).ljust(7, "0") + str(sequence_number).rjust(
            5, "0"
        )
        return self._ean13_with_checksum(ean12)

    @api.model
    def _get_barcode_sequence(self, company):
        sequences = self.env["ir.sequence"].search(
            [
                ("code", "=", "barcode.sequence"),
                ("company_id", "in", [company.id, False]),
            ]
        )
        if not sequences:
            return self.env["ir.sequence"].create(
                {
                    "name": "Barcode sequence",
                    "code": "barcode.sequence",
                    "implementation": "no_gap",
                    "padding": 5,
                    "number_next": 1,
                    "number_increment": 1,
                }
            )
        return max(sequences, key=lambda seq: seq.number_next_actual)

    @api.model
    def _ean13_with_checksum(self, ean12):
        if len(ean12) != 12:
            raise UserError(
                _("An EAN13 barcode needs exactly 12 digits before the check digit.")
            )
        odd_position_sum = sum(int(digit) for digit in ean12[::2])
        even_position_sum = sum(int(digit) for digit in ean12[1::2])
        check_digit = (10 - (odd_position_sum + even_position_sum * 3) % 10) % 10
        return ean12 + str(check_digit)
