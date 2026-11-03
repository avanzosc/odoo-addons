# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductCode(models.Model):
    _name = "product.code"
    _description = "Product Reference Coding"
    _order = "name"

    name = fields.Char(required=True, copy=False)
    brand_id = fields.Many2one(comodel_name="product.brand")
    family_id = fields.Many2one(comodel_name="product.category")
    sub_family_id = fields.Many2one(comodel_name="product.category", string="Subfamily")
    season_id = fields.Many2one(comodel_name="seasonality")
    sequence_id = fields.Many2one(comodel_name="ir.sequence", required=True)
    sequence_number_next = fields.Integer(
        string="Next Number",
        compute="_compute_sequence_number_next",
        inverse="_inverse_sequence_number_next",
        help="The next number that will be used to build a product "
        "reference for this combination of brand, family, subfamily and "
        "season.",
    )

    @api.depends("sequence_id.use_date_range", "sequence_id.number_next_actual")
    def _compute_sequence_number_next(self):
        for code in self:
            sequence = code.sequence_id._get_current_sequence()
            code.sequence_number_next = sequence.number_next_actual if sequence else 1

    def _inverse_sequence_number_next(self):
        for code in self:
            if code.sequence_id and code.sequence_number_next:
                sequence = code.sequence_id._get_current_sequence()
                sequence.sudo().number_next = code.sequence_number_next

    @api.model
    def _build_prefix(self, brand, family, sub_family, season):
        return "".join(
            [
                brand.code if brand else "00",
                family.code if family else "00",
                sub_family.code if sub_family else "00",
                season.code if season else "000",
            ]
        )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("sequence_id"):
                continue
            brand = self.env["product.brand"].browse(vals.get("brand_id"))
            family = self.env["product.category"].browse(vals.get("family_id"))
            sub_family = self.env["product.category"].browse(vals.get("sub_family_id"))
            season = self.env["seasonality"].browse(vals.get("season_id"))
            prefix = self._build_prefix(brand, family, sub_family, season)
            sequence = self.env["ir.sequence"].search([("name", "=", prefix)], limit=1)
            if not sequence:
                sequence = self.env["ir.sequence"].create(
                    {
                        "name": prefix,
                        "code": "product.product",
                        "implementation": "no_gap",
                        "prefix": prefix,
                        "padding": 3,
                        "use_date_range": False,
                    }
                )
            vals["sequence_id"] = sequence.id
            vals["name"] = prefix
        return super().create(vals_list)
