# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductCode(models.Model):
    _name = "product.code"
    _description = "Product Reference Coding"
    _order = "name"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        copy=False,
    )
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
    _sql_constraints = [
        (
            "name_uniq",
            "UNIQUE (brand_id, family_id, sub_family_id, season_id)",
            "The product code prefix must be unique.",
        ),
    ]

    @api.depends(
        "brand_id.code",
        "family_id.code",
        "sub_family_id.code",
        "season_id.code",
    )
    def _compute_name(self):
        for code in self:
            code.name = self._build_prefix(
                code.brand_id, code.family_id, code.sub_family_id, code.season_id
            )

    @api.depends("sequence_id.use_date_range", "sequence_id.number_next_actual")
    def _compute_sequence_number_next(self):
        for code in self:
            sequence = code.sequence_id._get_current_sequence()
            code.sequence_number_next = sequence.number_next_actual if sequence else 1

    def _inverse_sequence_number_next(self):
        for code in self:
            sequence = (
                code.sequence_id._get_current_sequence() if code.sequence_id else None
            )
            if sequence and code.sequence_number_next:
                sequence.sudo().number_next = code.sequence_number_next
                code.invalidate_recordset(["sequence_number_next"])

    @api.model
    def _build_prefix(self, brand, family, sub_family, season):
        return "".join(
            [
                (brand.code or "00") if brand else "00",
                (family.code or "00") if family else "00",
                (sub_family.code or "00") if sub_family else "00",
                (season.code or "000") if season else "000",
            ]
        )

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [dict(vals) for vals in vals_list]
        prefixes = {}
        for index, vals in enumerate(vals_list):
            vals.pop("name", None)
            if vals.get("sequence_id"):
                continue
            brand = self.env["product.brand"].browse(vals.get("brand_id"))
            family = self.env["product.category"].browse(vals.get("family_id"))
            sub_family = self.env["product.category"].browse(vals.get("sub_family_id"))
            season = self.env["seasonality"].browse(vals.get("season_id"))
            prefixes[index] = self._build_prefix(brand, family, sub_family, season)

        if prefixes:
            names = list(set(prefixes.values()))
            sequences = {
                sequence.name: sequence
                for sequence in self.env["ir.sequence"].search(
                    [("code", "=", "product.product"), ("name", "in", names)]
                )
            }
            missing = [name for name in names if name not in sequences]
            if missing:
                created = self.env["ir.sequence"].create(
                    [
                        {
                            "name": name,
                            "code": "product.product",
                            "implementation": "no_gap",
                            "prefix": name,
                            "padding": 3,
                            "use_date_range": False,
                        }
                        for name in missing
                    ]
                )
                sequences.update({sequence.name: sequence for sequence in created})
            for index, prefix in prefixes.items():
                vals_list[index]["sequence_id"] = sequences[prefix].id
        return super().create(vals_list)
