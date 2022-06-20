# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProductImport(models.Model):
    _name = "product.import"
    _inherit = "base.import"
    _description = "Wizard to import products"

    @api.model
    def _get_selection_product_type(self):
        return self.env["product.product"].fields_get(
            allfields=["type"])["type"]["selection"]

    import_line_ids = fields.One2many(
        comodel_name="product.import.line",
    )
    product_type = fields.Selection(
        selection="_get_selection_product_type",
        string="Default Product Type",
    )
    uom_id = fields.Many2one(
        string="Default Unit of Measure",
        comodel_name="uom.uom",
    )
    product_count = fields.Integer(
        string="# Products",
        compute="_compute_product_count",
    )

    def _get_line_values(self, row_values={}):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        product_name = row_values.get("Product Name", "")
        product_code = row_values.get("Product Code", "")
        category_name = row_values.get("Category Name", "")
        uom_name = row_values.get("UoM Name", "")
        log_info = ""
        if not product_name:
            if product_code:
                product_name = product_code
                log_info = _("Product Code added as Product Name")
            else:
                return {}
        values.update({
            "product_name": product_name,
            "product_default_code": product_code,
            "category_name": category_name,
            "product_uom": uom_name,
            "log_info": log_info,
        })
        if not uom_name and self.uom_id:
            values.update({
                "product_uom": self.uom_id.name,
                "product_uom_id": self.uom_id.id,
            })
        if self.product_type:
            values.update({
                "product_type": self.product_type,
            })
        return values

    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.mapped("import_line_ids.product_id"))

    def button_open_product(self):
        self.ensure_one()
        products = self.mapped("import_line_ids.product_id")
        action = self.env.ref("product.product_normal_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("id", "in", products.ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict


class ProductImportLine(models.Model):
    _name = "product.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import products"

    @api.model
    def _get_selection_product_type(self):
        return self.env["product.product"].fields_get(
            allfields=["type"])["type"]["selection"]

    def default_product_type(self):
        default_dict = self.env["product.product"].default_get(["type"])
        return default_dict.get("type")

    product_name = fields.Char(
        string="Product Name",
        required=True,
    )
    product_default_code = fields.Char(
        string="Internal Reference",
    )
    product_type = fields.Selection(
        selection="_get_selection_product_type",
        string="Product Type",
        default=default_product_type,
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    product_uom = fields.Char(
        string="Product Unit of Measure",
    )
    product_uom_id = fields.Many2one(
        string="Unit of Measure",
        comodel_name="uom.uom",
        domain="[('name','ilike',product_uom)]",
    )
    category_name = fields.Char(
        string="Product Category Name",
    )
    category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        domain="[('name','ilike',category_name)]",
    )
    sale_ok = fields.Boolean(
        string="Can be Sold",
        default=True,
    )
    purchase_ok = fields.Boolean(
        string="Can be Purchased",
        default=True,
    )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            category = uom = False
            product, log_info = line._check_product()
            if not log_info:
                category, log_info = line._check_category()
            if not log_info:
                uom, log_info = line._check_uom()
            state = "error" if log_info else "pass"
            line_values.append((1, line.id, {
                "product_id": product.id,
                "category_id": category and category.id,
                "product_uom_id": uom and uom.id,
                "log_info": log_info,
                "state": state,
            }))
        return line_values

    def action_process(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            product, log_info = line._create_product()
            state = "error" if log_info else "done"
            line_values.append((1, line.id, {
                "product_id": product.id,
                "log_info": log_info,
                "state": state,
            }))
        return line_values

    def _check_product(self):
        self.ensure_one()
        product_obj = self.env["product.product"]
        search_domain = [("name", "=", self.product_name)]
        log_info = ""
        if self.product_default_code:
            search_domain = expression.AND(
                [[("default_code", "=", self.product_default_code)], search_domain]
            )
        products = product_obj.search(search_domain)
        if len(products) > 1:
            log_info = _("Error: More than one product already exist")
        return products[:1], log_info

    def _check_category(self):
        self.ensure_one()
        log_info = ""
        if self.category_id:
            return self.category_id, log_info
        category_obj = self.env["product.category"]
        search_domain = [("name", "=", self.product_name)]
        categories = category_obj.search(search_domain)
        if len(categories) > 1:
            log_info = _("Error: More than one product category exist")
        return categories[:1], log_info

    def _check_uom(self):
        self.ensure_one()
        log_info = ""
        if self.product_uom_id:
            return self.product_uom_id, log_info
        uom_obj = self.env["uom.uom"]
        search_domain = [("name", "ilike", self.product_uom)]
        uoms = uom_obj.search(search_domain)
        if not uoms:
            log_info = _("Error: Unit of measure not found")
        elif len(uoms) != 1:
            log_info = _("Error: More than one unit of measure exist")
        return uoms[:1], log_info

    def _create_product(self):
        self.ensure_one()
        product, log_info = self._check_product()
        if not product and not log_info:
            product_obj = self.env["product.product"]
            product = product_obj.create({
                "name": self.product_name,
                "default_code": self.product_default_code,
                "uom_id": self.product_uom_id.id,
                "uom_po_id": self.product_uom_id.id,
                "categ_id": self.category_id.id,
                "type": self.product_type,
            })
            log_info = ""
        return product, log_info
