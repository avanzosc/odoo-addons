# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from functools import reduce

from odoo import _, api, fields, models
from odoo.exceptions import UserError

COMPOSITION_ATTRIBUTES = (
    ("Top", "T"),
    ("M2", "M2"),
    ("M3", "M3"),
    ("M4", "M4"),
    ("M5", "M5"),
    ("M6", "M6"),
    ("Bottom", "B"),
)


class InternalProductCategory(models.Model):
    _name = "internal.product.category"
    _description = "Internal Product Category"

    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "internal_category_name_unique",
            "unique(name)",
            "Internal product category name must be unique.",
        )
    ]


class ProductSeries(models.Model):
    _name = "product.series"
    _description = "Product Series"

    name = fields.Char(required=True, index=True)

    _sql_constraints = [
        (
            "series_name_unique",
            "unique(name)",
            "Product series name must be unique.",
        )
    ]


class ProductSeason(models.Model):
    _name = "product.season"
    _description = "Product seasons"
    _order = "name"

    name = fields.Char(size=3, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name"):
                vals["name"] = vals["name"].rjust(3, "0")
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("name"):
            vals["name"] = vals["name"].rjust(3, "0")
        return super().write(vals)


class ProductCode(models.Model):
    _name = "product.code"
    _description = "Product codes"
    _order = "name"

    name = fields.Char(required=True)
    family_id = fields.Many2one(comodel_name="product.category", string="Family")
    brand_id = fields.Many2one(comodel_name="product.brand", string="Brand")
    sub_family_id = fields.Many2one(comodel_name="product.category", string="Subfamily")
    season_id = fields.Many2one(comodel_name="product.season", string="Season")
    sequence_id = fields.Many2one(
        comodel_name="ir.sequence", string="Sequence", required=True
    )
    sequence_number_next = fields.Integer(
        string="Next Number",
        help="The next sequence number will be used for the next Code.",
        compute="_compute_seq_number_next",
        inverse="_inverse_seq_number_next",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("sequence_id"):
                prefix = self._get_prefix_from_values(vals)
                sequence = self.env["ir.sequence"].search(
                    [("name", "=", prefix)], limit=1
                )
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

    def _get_prefix_from_values(self, vals):
        family_code = brand_code = sub_family_code = "00"
        season_code = "000"
        if vals.get("family_id"):
            family_code = self.env["product.category"].browse(vals["family_id"]).code
        if vals.get("brand_id"):
            brand_code = self.env["product.brand"].browse(vals["brand_id"]).code
        if vals.get("sub_family_id"):
            sub_family_code = (
                self.env["product.category"].browse(vals["sub_family_id"]).code
            )
        if vals.get("season_id"):
            season_code = self.env["product.season"].browse(vals["season_id"]).name
        return (
            f"{brand_code or '00'}{family_code or '00'}"
            f"{sub_family_code or '00'}{season_code or '000'}"
        )

    @api.depends("sequence_id.number_next_actual")
    def _compute_seq_number_next(self):
        for code in self:
            code.sequence_number_next = (
                code.sequence_id.number_next_actual if code.sequence_id else 1
            )

    def _inverse_seq_number_next(self):
        for code in self:
            if code.sequence_id and code.sequence_number_next:
                code.sequence_id.sudo().number_next = code.sequence_number_next


class ResCompany(models.Model):
    _inherit = "res.company"

    barcode_prefix = fields.Integer(
        string="Company barcode prefix",
        help="Used by barcode generator. The number must have 7 digits as maximun",
    )
    include_attributes = fields.Boolean(string="Include attributes in the product code")

    @api.onchange("barcode_prefix")
    def _onchange_barcode_prefix(self):
        if self.barcode_prefix > 9999999:
            raise UserError(_("The barcode prefix must have 7 digits as maximun."))


class ProductBrand(models.Model):
    _inherit = "product.brand"

    code = fields.Char(size=2, required=True, default="00")

    def write(self, vals):
        if vals.get("code"):
            vals["code"] = vals["code"].rjust(2, "0")
        return super().write(vals)


class ProductCategory(models.Model):
    _inherit = "product.category"

    code = fields.Char(size=2, required=True, default="00")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("code") or vals["code"] == "00":
                vals["code"] = vals.get("name", "").rjust(2, "0")
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("code"):
            vals["code"] = vals["code"].rjust(2, "0")
        return super().write(vals)


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    code = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("code") and vals.get("name"):
                vals["code"] = vals["name"][:3]
        return super().create(vals_list)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    family_id = fields.Many2one(comodel_name="product.category", string="Family")
    internal_category_id = fields.Many2one(
        comodel_name="internal.product.category", string="Internal Category"
    )
    season_id = fields.Many2one(comodel_name="product.season", string="Season")
    serie_id = fields.Many2one(comodel_name="product.series", string="Product serie")
    sub_family_id = fields.Many2one(comodel_name="product.category", string="Subfamily")

    def generate_code(self):
        for template in self:
            template.product_variant_ids.generate_code()

    @api.onchange("family_id", "sub_family_id")
    def _onchange_family(self):
        if self.family_id:
            self.categ_id = self.sub_family_id or self.family_id
        else:
            self.categ_id = False


class ProductProduct(models.Model):
    _inherit = "product.product"

    composition = fields.Char(
        compute="_compute_composition",
        store=True,
    )

    @api.depends(
        "product_template_attribute_value_ids.product_attribute_value_id",
        "product_template_attribute_value_ids.product_attribute_value_id.code",
    )
    def _compute_composition(self):
        attribute_obj = self.env["product.attribute"]
        attributes = {
            name: attribute_obj.search([("name", "=ilike", name)], limit=1)
            for name, __ in COMPOSITION_ATTRIBUTES
        }
        for product in self:
            values = (
                product.product_template_attribute_value_ids.product_attribute_value_id
            )
            composition_parts = []
            for attribute_name, prefix in COMPOSITION_ATTRIBUTES:
                value = values.filtered(
                    lambda attribute_value, name=attribute_name: (
                        attribute_value.attribute_id == attributes[name]
                    )
                )[:1]
                if value and value.code:
                    composition_parts.append(f"{prefix}{value.code[-2:]}")
            product.composition = "".join(composition_parts)

    def generate_code(self):
        for product in self:
            product._generate_code()

    def _generate_code(self):
        for product in self:
            if not product.default_code:
                product.default_code = product._get_next_default_code()
            if not product.barcode:
                product.barcode = product._get_next_ean13_barcode()

    def _get_next_default_code(self):
        self.ensure_one()
        product_code_model = self.env["product.code"]
        prefix = self._get_default_code_prefix()
        product_code = product_code_model.search([("name", "=", prefix)], limit=1)
        attributes_code = self._get_attributes_code()
        if not product_code:
            product_code = product_code_model.create(
                {
                    "family_id": self.family_id.id,
                    "brand_id": self.product_brand_id.id,
                    "sub_family_id": self.sub_family_id.id,
                    "season_id": self.season_id.id,
                }
            )
        return product_code.sequence_id.with_context(
            attributes_code=attributes_code
        ).next_by_id()

    def _get_default_code_prefix(self):
        self.ensure_one()
        family_code = self.family_id.code or "00"
        brand_code = self.product_brand_id.code or "00"
        sub_family_code = self.sub_family_id.code or "00"
        season_code = self.season_id.name or "000"
        return f"{brand_code}{family_code}{sub_family_code}{season_code}"

    def _get_attributes_code(self):
        self.ensure_one()
        attribute_values = (
            self.product_template_attribute_value_ids.product_attribute_value_id
        )
        attributes_code = "".join(
            (attribute.code or "000") for attribute in attribute_values[:3]
        )
        return attributes_code.ljust(9, "0")

    def _get_next_ean13_barcode(self):
        self.ensure_one()
        if not self.env.company.barcode_prefix:
            raise UserError(
                _(
                    "Error in generating barcode. Please set the Company barcode "
                    "prefix in the Company configuration form."
                )
            )
        code_base = self.env["ir.sequence"].next_by_code("barcode.sequence")
        barcode_prefix = str(self.env.company.barcode_prefix).ljust(7, "0")
        barcode_sequence = str(code_base).rjust(5, "0")
        ean12 = f"{barcode_prefix}{barcode_sequence}"
        return self.calculate_checksum(ean12)

    def calculate_checksum(self, ean):
        if len(ean) != 12:
            raise UserError(
                _(
                    "The barcode must have 12 digits to calculate the checksum. "
                    "Please check the Barcode prefix on the company or the id of "
                    "the product.\n EAN12 = 0000000 + 00000 (prefix company "
                    "filled with 0 + product id filled with 0).\nEAN13 = EAN12 "
                    "+ 0 (Checksum)."
                )
            )
        evensum = reduce(lambda x, y: int(x) + int(y), ean[::2])
        oddsum = reduce(lambda x, y: int(x) + int(y), ean[1::2])
        return ean + str((10 - ((evensum + oddsum * 3) % 10)) % 10)
