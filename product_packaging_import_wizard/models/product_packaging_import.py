# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
import packaging
from itertools import product


class ProductPackagingImport(models.Model):
    _name = "product.packaging.import"
    _inherit = "base.import"
    _description = "Wizard to import product packagings"


    import_line_ids = fields.One2many(
        comodel_name="product.packaging.import.line",
    )
    packaging_count = fields.Integer(
        string="Packaging",
        compute="_compute_packaging_count",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company.id)

    def _get_line_values(self, row_values={}):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        product_name = row_values.get("Product Name", "")
        product_code = row_values.get("Product Code", "")
        packaging_name = row_values.get("Packaging Name", "")
        barcode = row_values.get("Barcode", "")
        quantity = row_values.get("Quantity", "")
        max_weight = row_values.get("Max Weight", "")
        weight = row_values.get("Weight", "")
        length = row_values.get("Length", "")
        width = row_values.get("Width", "")
        height = row_values.get("Height", "")
        log_info = ""
        if not product_name:
            if product_code:
                product_name = product_code
                log_info = _("Product Code added as Product Name")
            else:
                return {}
        if not packaging_name:
            log_info = _("Packaging Name is Required")
        values.update(
            {
                "product_name": product_name,
                "product_default_code": convert2str(product_code),
                "packaging_name": packaging_name,
                "barcode": convert2str(barcode),
                "quantity": quantity,
                "max_weight": max_weight,
                "weight": weight,
                "length": length,
                "width": width,
                "height": height,
                "log_info": log_info,
            }
        )
        return values

    def _compute_packaging_count(self):
        for record in self:
            record.packaging_count = len(
                record.mapped("import_line_ids.product_packaging_id"))

    def button_open_product_packaging(self):
        self.ensure_one()
        packagings = self.mapped("import_line_ids.product_packaging_id")
        action = self.env.ref("product.action_packaging_view")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", packagings.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class ProductPackagingImportLine(models.Model):
    _name = "product.packaging.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import product packagings"

    import_id = fields.Many2one(
        comodel_name="product.packaging.import",
    )
    action = fields.Selection(
        string="Action",
        selection=[
            ("create", "Create"),
            ("update", "Update"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    product_name = fields.Char(
        string="Product Name",
        required=True,
    )
    product_default_code = fields.Char(
        string="Internal Reference",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    packaging_name = fields.Char(
        string="Packaging Name",
        )
    product_packaging_id = fields.Many2one(
        string="Product Packaging",
        comodel_name="product.packaging",
    )
    barcode = fields.Char(
        string="Barcode",
        )
    quantity = fields.Float(
        string="Quantity",
        )
    max_weight = fields.Float(
        string="Max Weight",
        )
    weight = fields.Float(
        string="Weight",
        )
    length = fields.Float(
        string="Length",
        )
    width = fields.Float(
        string="Width",
        )
    height = fields.Float(
        string="Height",
        )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            product = packaging = False
            product, log_info_product = line._check_product()
            if log_info_product:
                log_info += log_info_product
            if product:
                packaging, log_info_packaging = line._check_packaging(
                    product=product)
                if log_info_packaging:
                    log_info += log_info_packaging
            state = "error" if log_info else "pass"
            action = "nothing"
            if packaging and state != "error":
                action = "update"
            elif state != "error":
                action = "create"
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "product_id": product.id,
                        "product_packaging_id": packaging and packaging.id,
                        "log_info": log_info,
                        "state": state,
                        "action": action,
                    },
                )
            )
        return line_values

    def action_process(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            if line.action == "create":
                packaging, log_info = line._create_packaging(product=line.product_id)
            elif line.action == "update":
                packaging, log_info = line._update_packaging()
            else:
                continue
            state = "error" if log_info else "done"
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "product_packaging_id": packaging,
                        "log_info": log_info,
                        "state": state,
                    },
                )
            )
        return line_values

    def _check_product(self):
        self.ensure_one()
        product_obj = self.env["product.product"]
        search_domain = [("name", "=", self.product_name)]
        log_info = ""
        if self.product_default_code:
            search_domain = expression.AND(
                [[("default_code", "=", self.product_default_code)],
                 search_domain])
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: Product not found.")
        if len(products) > 1:
            products = False
            log_info = _("Error: More than one product found.")
        return products[:1], log_info

    def _check_packaging(self, product=False):
        self.ensure_one()
        packaging_obj = self.env["product.packaging"]
        search_domain = [("name", "=", self.packaging_name)]
        log_info = ""
        if product:
            search_domain = expression.AND([[
                ("product_id", "=", product.id)], search_domain])
        packagings = packaging_obj.search(search_domain)
        if len(packagings) > 1:
            packagings = False
            log_info = _("Error: More than one packaging found.")
        return packagings[:1], log_info

    def _create_packaging(self, product=False):
        self.ensure_one()
        packaging, log_info = self._check_packaging(product=product)
        if not packaging and not log_info:
            packaging_obj = self.env["product.packaging"]
            values = self._packaging_values()
            values.update({
                "name": self.packaging_name})
            packaging = packaging_obj.create(values)
            log_info = ""
        return packaging, log_info

    def _update_packaging(self):
        self.ensure_one()
        packaging = self.product_packaging_id
        values = self._packaging_values()
        packaging.write(values)
        log_info = ""
        return packaging, log_info

    def _packaging_values(self):
        self.ensure_one()
        return {
            "product_id": self.product_id.id,
            "barcode": self.barcode,
            "qty": self.quantity,
            "max_weight": self.max_weight,
            "weight": self.weight,
            "packaging_length": self.length,
            "width": self.width,
            "height": self.height,
            "company_id": self.import_id.company_id.id,
            }
