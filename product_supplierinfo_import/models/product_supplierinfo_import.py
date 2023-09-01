# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
import unicodedata
import xlrd


class ProductSupplierinfoImport(models.Model):
    _name = "product.supplierinfo.import"
    _inherit = "base.import"
    _description = "Supplier Rate Import"

    import_line_ids = fields.One2many(
        comodel_name="product.supplierinfo.import.line",
    )
    product_supplierinfo_count = fields.Integer(
        string="Supplier Rate",
        compute="_compute_product_supplierinfo_count",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company.id,
    )
    supplier_id = fields.Many2one(
        string="Default Supplier",
        comodel_name="res.partner",
    )
    currency_id = fields.Many2one(
        string="Default Currency",
        comodel_name="res.currency"
    )
    date_start = fields.Date(
        string="Default Date Start"
    )
    date_end = fields.Date(
        string="Default Date End"
    )
    product_found_reference = fields.Boolean(
        string="Found Product Only By Internal Reference",
        default=False
    )
    supplier_found_reference = fields.Boolean(
        string="Found Supplier Only By Reference",
        default=False
    )

    @api.onchange("supplier_id")
    def _onchange_supplier_id(self):
        if self.supplier_id:
            for line in self.import_line_ids.filtered(
                lambda c: not c.supplier_code and not (
                    c.supplier_name)):
                line.supplier_id = self.supplier_id.id
                line.supplier_code = self.supplier_id.ref
                line.supplier_name = self.supplier_id.name

    @api.onchange("currency_id")
    def _onchange_currency_id(self):
        if self.currency_id:
            for line in self.import_line_ids.filtered(
                lambda c: not (
                    c.currency)):
                line.currency = self.currency_id.name
                line.currency_id = self.currency_id.id

    @api.onchange("date_start")
    def _onchange_date_start(self):
        if self.date_start:
            for line in self.import_line_ids.filtered(
                lambda c: not (
                    c.date_start)):
                line.date_start = self.date_start

    @api.onchange("date_end")
    def _onchange_date_end(self):
        if self.date_end:
            for line in self.import_line_ids.filtered(
                lambda c: not (
                    c.date_end)):
                line.date_end = self.date_end

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            supplier_code = row_values.get("Supplier Code", "")
            supplier_name = row_values.get("Supplier Name", "")
            product_code = row_values.get("Product Code", "")
            product_name = row_values.get("Product Name", "")
            supplier_product_code = row_values.get("Supplier Product Code", "")
            supplier_product_name = row_values.get("Supplier Product Name", "")
            quantity = row_values.get("Quantity", "")
            price = row_values.get("Price", "")
            discount = row_values.get("Discount", "")
            delay = row_values.get("Delay", "")
            currency = row_values.get("Currency", "")
            date_start = row_values.get("Date Start", "")
            date_end = row_values.get("Date End", "")
            if date_start:
                date_start = xlrd.xldate.xldate_as_datetime(date_start, 0)
                date_start = date_start.date()
            elif not date_start:
                date_start = False
            if date_end:
                date_end = xlrd.xldate.xldate_as_datetime(date_end, 0)
                date_end = date_end.date()
            elif not date_end:
                date_end = False
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
                    "currency": currency,
                    "date_start": date_start,
                    "date_end": date_end,
                    "log_info": log_info,
                }
            )
            if not supplier_code and not supplier_name and self.supplier_id:
                values.update(
                {
                    "supplier_code": self.supplier_id.ref,
                    "supplier_name": self.supplier_id.name,
                    "supplier_id": self.supplier_id.id
                })
            if not currency and self.currency_id:
                values.update(
                {
                    "currency": self.currency_id.id,
                    "currency_id": self.currency_id.id
                })
            if not date_start and self.date_start:
                values.update(
                {
                    "date_start": self.date_start,
                })
            if not date_end and self.date_end:
                values.update(
                {
                    "date_end": self.date_end,
                })
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
    currency = fields.Char(
        string="Currency Name",
        )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        )
    date_start = fields.Date(
        string="Date Start",
        )
    date_end = fields.Date(
        string="Date End",
        )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            supplier = product = supplierinfo = currency = False
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
            if line.currency:
                currency, log_info_currency = line._check_currency()
                if log_info_currency:
                    log_info += log_info_currency
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
                "currency_id": currency and currency.id,
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
        if (
            self.supplier_code and not self.supplier_name) or (
                self.import_id.supplier_found_reference):
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
        if (
            self.product_code and not self.product_name) or (
                self.import_id.product_found_reference):
            search_domain = [
                ("default_code", "=", self.product_code)]
        elif self.product_name and not self.product_code:
            search_domain = [("trim_name", "=", name)]
        elif self.product_code and self.product_name:
            search_domain = [
                ("trim_name", "=ilike", name),
                ("default_code", "=", self.product_code)]
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
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
            search_domain = [
                ("name", "=", supplier.id),
                ("product_tmpl_id", "=", product.product_tmpl_id.id)]
            supplierinfo = supplierinfo_obj.search(search_domain)
            if not supplierinfo:
                supplierinfo = False
            elif len(supplierinfo) > 1:
                supplierinfo = False
                log_info = _(
                    "Error: More than one product supplierinfo found.")
        return supplierinfo and supplierinfo[:1], log_info

    def _check_currency(self):
        self.ensure_one()
        log_info = ""
        if self.currency_id:
            return self.currency_id, log_info
        currency_obj = self.env["res.currency"]
        search_domain = [("name", "=", self.currency)]
        currency = currency_obj.search(search_domain)
        if not currency:
            currency = False
            log_info = _("Error: Currency not found.")
        elif len(currency) > 1:
            currency = False
            log_info = _("Error: More than one currency found.")
        return currency and currency[:1], log_info

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
            "currency_id": self.currency_id.id,
            "date_start": self.date_start,
            "date_end": self.date_end,
        }

    def _update_supplierinfo(self):
        self.ensure_one()
        values = self._supplierinfo_values()
        self.product_supplierinfo_id.write(values)
        log_info = ""
        return self.product_supplierinfo_id, log_info
