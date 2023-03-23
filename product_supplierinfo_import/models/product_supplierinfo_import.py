# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
import unicodedata


class ProductSupplierinfoImport(models.Model):
    _name = "product.supplierinfo.import"
    _inherit = "base.import"
    _description = "Supplier Rate Import"

    import_line_ids = fields.One2many(
        comodel_name="product.supplierinfo.import.line",
    )
    product_supplierinfo_count = fields.Integer(
        string="# Supplier Rate",
        compute="_compute_product_supplierinfo_count",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
    )

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            supplier_code = row_values.get("suppliercode", "")
            supplier_name = row_values.get("suppliername", "")
            product_code = row_values.get("productcode", "")
            product_name = row_values.get("productname", "")
            supplier_product_code = row_values.get("supplierproductcode", "")
            supplier_product_name = row_values.get("supplierproductname", "")
            quantity = row_values.get("quantity", "")
            price = row_values.get("price", "")
            discount = row_values.get("discount", "")
            delay = row_values.get("delay", "")
            log_info = ""
            values.update(
                {
                    "supplier_code": convert2str(supplier_code),
                    "supplier_name": supplier_name.title(),
                    "product_code": convert2str(product_code),
                    "product_name": convert2str(product_name),
                    "supplier_product_code": convert2str(
                        supplier_product_code),
                    "supplier_product_name": convert2str(
                        supplier_product_name),
                    "quantity": quantity,
                    "price": price,
                    "discount": discount,
                    "delay": delay,
                    "log_info": log_info,
                }
            )
        return values

    def _compute_product_supplierinfo_count(self):
        for record in self:
            record.product_supplierinfo_count = len(
                record.mapped("import_line_ids.product_supplierinfo_id"))

    def button_open_product_supplierinfo(self):
        self.ensure_one()
        line = self.mapped("import_line_ids.product_supplierinfo_id")
        action = self.env.ref("product.product_supplierinfo_type_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", line.ids)], safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict


class ProductSupplierinfoImportLine(models.Model):
    _name = "product.supplierinfo.import.line"
    _inherit = "base.import.line"
    _description = "Supplier Rate Import Line"

    @api.model
    def _get_selection_supplierinfo_type(self):
        return self.env["product.supplierinfo"].fields_get(
            allfields=["type"])["type"]["selection"]

    def default_supplierinfo_type(self):
        default_dict = self.env["product.supplierinfo"].default_get(["type"])
        return default_dict.get("type")

    import_id = fields.Many2one(
        comodel_name="product.supplierinfo.import",
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
    product_supplierinfo_id = fields.Many2one(
        string="Product Suplierinfo",
        comodel_name="product.supplierinfo",
        states={"done": [("readonly", True)]},
        copy=False,)
    supplier_code = fields.Char(
        string="Supplier Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    supplier_name = fields.Char(
        string="Supplier Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_name = fields.Char(
        string="Product Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    supplier_product_code = fields.Char(
        string="Supplier Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    supplier_product_name = fields.Char(
        string="Supplier Product Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    quantity = fields.Float(
        string="Quantity",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    price = fields.Float(
        string="Price",
        states={"done": [("readonly", True)]},
        copy=False,
        digits="Product Price",
    )
    discount = fields.Float(
        string="Discount",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delay = fields.Integer(
        string="Delay",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier",
        states={"done": [("readonly", True)]},
        copy=False,
        )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        states={"done": [("readonly", True)]},
        copy=False,
        )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            supplier = product = supplierinfo = False
            supplier, log_info_supplier = line._check_supplier()
            if log_info_supplier:
                log_info += log_info_supplier
            product, log_info_product = line._check_product()
            if log_info_product:
                log_info += log_info_product
            if not log_info_product and not log_info_supplier:
                supplierinfo, log_info_supplierinfo = line._check_supplierinfo(
                    product=product, supplier=supplier)
                if log_info_supplierinfo:
                    log_info += log_info_supplierinfo
            state = "error" if log_info else "pass"
            action = "nothing"
            if supplierinfo and state != "error":
                action = "update"
            elif state != "error":
                action = "create"
            update_values = {
                "supplier_id": supplier and supplier.id,
                "product_id": product and product.id,
                "product_supplierinfo_id": supplierinfo and supplierinfo.id,
                "log_info": log_info,
                "state": state,
                "action": action,
                }
            line_values.append(
                (
                    1,
                    line.id,
                    update_values,
                )
            )
        return line_values

    def action_process(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            if line.action == "create":
                supplierinfo, log_info = line._create_supplierinfo()
            elif line.action == "update":
                supplierinfo, log_info = line._update_supplierinfo()
            else:
                continue
            state = "error" if log_info else "done"
            update_values = {
                "product_supplierinfo_id": supplierinfo.id,
                "log_info": log_info,
                "state": state
                }
            line_values.append(
                (
                    1,
                    line.id,
                    update_values,
                )
            )
        return line_values

    def _check_supplier(self):
        self.ensure_one()
        log_info = ""
        if self.supplier_id:
            return self.supplier_id, log_info
        supplier_obj = self.env["res.partner"]
        search_domain = []
        if self.supplier_code and not self.supplier_name:
            search_domain = [("ref", "=", self.supplier_code)]
        elif self.supplier_name and not self.supplier_code:
            search_domain = [("name", "=ilike", self.supplier_name)]
        elif self.supplier_code and self.supplier_name:
            search_domain = [
                '|', ("name", "=ilike", self.supplier_name),
                ("ref", "=", self.supplier_code)]
        suppliers = supplier_obj.search(search_domain)
        if not suppliers:
            suppliers = False
            log_info = _("Error: No supplier found.")
        elif len(suppliers) > 1:
            if self.supplier_code and self.supplier_name:
                search_domain = [
                    ("name", "=ilike", self.supplier_name),
                    ("ref", "=", self.supplier_code)]
                suppliers = supplier_obj.search(search_domain)
                if not len(suppliers) == 1:
                    suppliers = False
                    log_info = _("Error: More than one supplier found.")
        return suppliers and suppliers[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.product_id:
            return self.product_id, log_info
        product_obj = self.env["product.product"]
        search_domain = []
        if self.product_name:
            name = self.product_name.replace(" ", "")
            name = ''.join((c for c in unicodedata.normalize(
                'NFD', name) if unicodedata.category(c) != 'Mn'))
        if self.product_code and not self.product_name:
            search_domain = [
                ("default_code", "=", self.product_code)]
        elif self.product_name and not self.product_code:
            search_domain = [("trim_name", "=ilike", name)]
        elif self.product_code and self.product_name:
            search_domain = [
                '|', ("trim_name", "=ilike", name),
                ("default_code", "=", self.product_code)]
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
            if self.product_code and self.product_name:
                search_domain = [
                    ("trim_name", "=ilike", name),
                    ("default_code", "=", self.product_code)]
                products = product_obj.search(search_domain)
                if not len(products) == 1:
                    products = False
                    log_info = _("Error: More than one product found.")
        return products and products[:1], log_info

    def _check_supplierinfo(self, product=False, supplier=False):
        self.ensure_one()
        log_info = ""
        supplierinfo = False
        if self.product_supplierinfo_id:
            return self.product_supplierinfo_id, log_info
        supplierinfo_obj = self.env["product.supplierinfo"]
        if product and supplier:
            search_domain = [("name", "=", supplier.id),
                ("product_tmpl_id", "=", product.product_tmpl_id.id)]
            supplierinfo = supplierinfo_obj.search(search_domain)
            if not supplierinfo:
                supplierinfo = False
            elif len(supplierinfo) > 1:
                supplierinfo = False
                log_info = _(
                    "Error: More than one product supplierinfo found.")
        return supplierinfo and supplierinfo[:1], log_info

    def _create_supplierinfo(self):
        self.ensure_one()
        supplierinfo, log_info = self._check_supplierinfo()
        if not supplierinfo and not log_info:
            supplierinfo_obj = self.env["product.supplierinfo"]
            values = self._supplierinfo_values()
            supplierinfo = supplierinfo_obj.create(values)
            log_info = ""
        return supplierinfo, log_info

    def _supplierinfo_values(self):
        return {
            "name": self.supplier_id.id,
            "product_tmpl_id": self.product_id.product_tmpl_id.id,
            "product_name": self.supplier_product_name,
            "product_code": self.supplier_product_code,
            "min_qty": self.quantity,
            "discount": self.discount,
            "price": self.price,
            "delay": self.delay,
            "company_id": self.import_id.company_id.id or self.env.company.id,
        }

    def _update_supplierinfo(self):
        self.ensure_one()
        values = self._supplierinfo_values()
        self.product_supplierinfo_id.write(values)
        log_info = ""
        return self.product_supplierinfo_id, log_info
