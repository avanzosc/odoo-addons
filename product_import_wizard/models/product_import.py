# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
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
        string="Products",
        compute="_compute_product_count",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company.id
    )
    product_found_reference = fields.Boolean(
        string="Found Product Only By Internal Reference",
        default=False
    )
    data = fields.Binary(
        required=False,
    )

    @api.onchange("uom_id")
    def _onchange_uom_id(self):
        if self.uom_id:
            for line in self.import_line_ids.filtered(
                lambda c: not c.product_uom and (
                    not c.product_uom_id)):
                line.product_uom = self.uom_id.name
                line.product_uom_id = self.uom_id.id

    def _get_line_values(self, row_values={}):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        product_name = row_values.get("Product Name", "")
        sale_ok = row_values.get("Sale OK", "")
        purchase_ok = row_values.get("Purchase OK", "")
        product_code = row_values.get("Product Code", "")
        product_type = row_values.get("Product Type", "")
        category_name = row_values.get("Category Name", "")
        barcode = row_values.get("Barcode", "")
        list_price = row_values.get("List Price", "")
        customer_tax = row_values.get("Customer Tax", "")
        standard_price = row_values.get("Standard Price", "")
        uom_name = row_values.get("UoM Name", "")
        purchase_uom_name = row_values.get("Purchase UoM Name", "")
        invoice_policy = row_values.get("Invoice Policy", "")
        purchase_method = row_values.get("Purchase Method", "")
        description_purchase = row_values.get("Description Purchase", "")
        property_account_income = row_values.get("Property Account Income", "")
        property_account_expense = row_values.get("Property Account Expense", "")
        log_info = ""
        state = "2validate"
        if sale_ok == "True":
            sale_ok = True
        elif sale_ok == "False":
            sale_ok = False
        elif sale_ok != "False" and sale_ok != "True":
            sale_ok = self.env["product.import.line"].default_sale_ok()
        if purchase_ok == "True":
            purchase_ok = True
        elif purchase_ok == "False":
            purchase_ok = False
        elif purchase_ok != "False" and purchase_ok != "True":
            purchase_ok = self.env["product.import.line"].default_purchase_ok()
        if product_type != "consu" and (
            product_type != "service") and (
                product_type != "product"):
            if product_type:
                log_info += _("Product Type not understood.")
            product_type = self.env[
                "product.import.line"].default_product_type()
        if purchase_method != "purchase" and purchase_method != "receive":
            if purchase_method:
                log_info += _("Purchase Method not understood.")
            purchase_method = self.env[
                "product.import.line"].default_purchase_method()
        if not product_name:
            if product_code:
                product_name = product_code
                log_info = _("Product Code added as Product Name")
            else:
                return {}
        if log_info:
            state = "error"
        values.update(
            {
                "product_name": product_name,
                "sale_ok": sale_ok,
                "purchase_ok": purchase_ok,
                "product_default_code": convert2str(product_code),
                "category_name": category_name,
                "product_type": product_type,
                "barcode": convert2str(barcode),
                "list_price": list_price,
                "customer_tax": customer_tax,
                "standard_price": standard_price,
                "product_uom": uom_name,
                "purchase_uom_name": purchase_uom_name,
                "invoice_policy": invoice_policy,
                "purchase_method": purchase_method,
                "description_purchase": description_purchase,
                "property_account_income": convert2str(
                    property_account_income),
                "property_account_expense": convert2str(
                    property_account_expense),
                "log_info": log_info,
                "state": state,
            }
        )
        if not uom_name and self.uom_id:
            values.update(
                {
                    "product_uom": self.uom_id.name,
                    "product_uom_id": self.uom_id.id,
                }
            )
        if self.product_type:
            values.update(
                {
                    "product_type": self.product_type,
                }
            )
        return values

    def _compute_product_count(self):
        for record in self:
            record.product_count = len(
                record.mapped("import_line_ids.product_id"))

    def button_open_product(self):
        self.ensure_one()
        products = self.mapped("import_line_ids.product_id")
        action = self.env.ref("product.product_normal_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", products.ids)], safe_eval(action.domain or "[]")]
        )
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

    @api.model
    def _get_selection_purchase_method(self):
        return self.env["product.product"].fields_get(
            allfields=["purchase_method"])["purchase_method"]["selection"]

    @api.model
    def _get_selection_invoice_policy(self):
        return self.env["product.product"].fields_get(
            allfields=["invoice_policy"]
        )["invoice_policy"]["selection"]

    def default_product_type(self):
        default_dict = self.env["product.product"].default_get(["type"])
        return default_dict.get("type")

    def default_sale_ok(self):
        default_dict = self.env["product.product"].default_get(["sale_ok"])
        return default_dict.get("sale_ok")

    def default_purchase_ok(self):
        default_dict = self.env["product.product"].default_get(["purchase_ok"])
        return default_dict.get("purchase_ok")

    def default_invoice_policy(self):
        default_dict = self.env["product.product"].default_get(
            ["invoice_policy"])
        return default_dict.get("invoice_policy")

    def default_purchase_method(self):
        default_dict = self.env["product.product"].default_get(
            ["purchase_method"])
        return default_dict.get("purchase_method")

    import_id = fields.Many2one(
        comodel_name="product.import",
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
    barcode = fields.Char(
        string="Barcode",
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
        string="Product UoM",
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
        default=default_sale_ok,
        )
    purchase_ok = fields.Boolean(
        string="Can be Purchased",
        )
    list_price = fields.Float(
        string="List Price",
        )
    customer_tax = fields.Char(
        string="Customer Tax Name")
    standard_price = fields.Float(
        string="Standard Price",
        )
    purchase_uom_name = fields.Char(
        string="Purchase UoM Name")
    invoice_policy = fields.Selection(
        selection="_get_selection_invoice_policy",
        string="Invoice Policy",
        default=default_invoice_policy,
    )
    purchase_uom_id = fields.Many2one(
        string="Purchase UoM",
        comodel_name="uom.uom",
        domain="[('name','ilike',purchase_uom_name)]",
    )
    customer_tax_id = fields.Many2one(
        string="Customer Tax",
        comodel_name="account.tax",
        domain="[('name','ilike',customer_tax)]",
        )
    purchase_method = fields.Selection(
        selection="_get_selection_purchase_method",
        string="Purchase Method",
        default=default_purchase_method,
    )
    description_purchase = fields.Text(
        string="Description Purchase",
        )
    property_account_income = fields.Char(
        string="Property Account Income Name",
        )
    property_account_income_id = fields.Many2one(
        string="Property Account Income",
        comodel_name="account.account",
        )
    property_account_expense = fields.Char(
        string="Property Account Expense Name",
        )
    property_account_expense_id = fields.Many2one(
        string="Property Account Expense",
        comodel_name="account.account",
        )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            category = uom = purchase_uom = tax = (
                    property_account_income) = property_account_expense= False
            product, log_info_product = line._check_product()
            if log_info_product:
                log_info += log_info_product
            category, log_info_category = line._check_category()
            if log_info_category:
                log_info += log_info_category
            uom, log_info_uom = line._check_uom(uom_name=line.product_uom)
            if log_info_uom:
                log_info += log_info_uom
            if line.purchase_uom_name:
                purchase_uom, log_info_purchase_uom = line._check_uom(
                    uom_name=line.purchase_uom_name)
                if log_info_purchase_uom:
                    log_info += log_info_purchase_uom
            if line.customer_tax:
                tax, log_info_tax = line._check_tax()
                if log_info_tax:
                    log_info += log_info_tax
            if line.barcode:
                log_info_barcode = line._check_barcode()
                if log_info_barcode:
                    log_info += log_info_barcode
            if line.property_account_income:
                property_account_income, log_info_property_account_income = (
                    line._check_property_account_income())
                if log_info_property_account_income:
                    log_info += log_info_property_account_income
            if line.property_account_expense:
                property_account_expense, log_info_property_account_expense = (
                    line._check_property_account_expense())
                if log_info_property_account_expense:
                    log_info += log_info_property_account_expense
            state = "error" if log_info else "pass"
            action = "nothing"
            if product and state != "error":
                action = "update"
            elif state != "error":
                action = "create"
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "product_id": product and product.id,
                        "category_id": category and category.id,
                        "product_uom_id": uom and uom.id,
                        "purchase_uom_id": purchase_uom and purchase_uom.id,
                        "customer_tax_id": tax and tax.id,
                        "property_account_income_id": (
                            property_account_income) and (
                                property_account_income.id),
                        "property_account_expense_id": (
                            property_account_expense) and (
                                property_account_expense.id),
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
            product = False
            if line.action == "create":
                product, log_info = line._create_product()
            elif line.action == "update":
                product, log_info = line._update_product()
            else:
                continue
            state = "error" if log_info else "done"
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "product_id": product.id,
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
        if self.import_id.product_found_reference:
            search_domain = [("default_code", "=", self.product_default_code)]
        products = product_obj.search(search_domain)
        if len(products) > 1:
            products = False
            log_info = _("Error: More than one product already exist.")
        return products, log_info

    def _check_category(self):
        self.ensure_one()
        log_info = ""
        if self.category_id:
            return self.category_id, log_info
        category_obj = self.env["product.category"]
        search_domain = [("name", "=", self.category_name)]
        categories = category_obj.search(search_domain)
        if not categories:
            categories = False
            log_info = _("Error: Product category not found.")
        elif len(categories) > 1:
            categories = False
            log_info = _("Error: More than one product category exist.")
        return categories, log_info

    def _check_uom(self, uom_name=False):
        self.ensure_one()
        log_info = ""
        if self.product_uom_id:
            return self.product_uom_id, log_info
        uom_obj = self.env["uom.uom"]
        search_domain = [("name", "ilike", uom_name)]
        uoms = uom_obj.search(search_domain)
        if not uoms:
            uoms = False
            log_info = _("Error: Unit of measure not found.")
        elif len(uoms) > 1:
            uoms = False
            log_info = _("Error: More than one unit of measure exist.")
        return uoms, log_info

    def _check_tax(self):
        self.ensure_one()
        log_info = ""
        if self.customer_tax_id:
            return self.customer_tax_id, log_info
        if not self.customer_tax:
            return False, log_info
        tax_obj = self.env["account.tax"]
        search_domain = [("name", "ilike", self.customer_tax)]
        taxes = tax_obj.search(search_domain)
        if not taxes:
            taxes = False
            log_info = _("Error: Tax not found.")
        elif len(taxes) > 1:
            taxes = False
            log_info = _("Error: More than one taxes found.")
        return taxes, log_info

    def _check_barcode(self):
        self.ensure_one()
        log_info = ""
        if self.barcode:
            same_barcode = self.import_id.import_line_ids.filtered(
                lambda c: c.barcode == self.barcode and c.id != self.id)
            if same_barcode:
                log_info = (
                    _("Error: There are other lines in this importer with the same barcode."))
            same_barcode = self.env["product.product"].search([
                ("name", "!=", self.product_name),
                ("barcode", "=", self.barcode)])
            if same_barcode:
                log_info = (
                    _("Error: Another product with the same barcode exists in the system."))
            return log_info

    def _check_property_account_income(self):
        self.ensure_one()
        log_info = ""
        if self.property_account_income_id:
            return self.property_account_income_id, log_info
        accunt_obj = self.env["account.account"]
        search_domain = [("code", "=", self.property_account_income)]
        accounts = accunt_obj.search(search_domain)
        if not accounts:
            accounts = False
            log_info = _("Error: Property account income not found.")
        elif len(accounts) > 1:
            accounts = False
            log_info = _("Error: More than one property account income found.")
        return accounts, log_info

    def _check_property_account_expense(self):
        self.ensure_one()
        log_info = ""
        if self.property_account_expense_id:
            return self.property_account_expense_id, log_info
        accunt_obj = self.env["account.account"]
        search_domain = [("code", "=", self.property_account_expense)]
        accounts = accunt_obj.search(search_domain)
        if not accounts:
            accounts = False
            log_info = _("Error: Property account expense not found.")
        elif len(accounts) > 1:
            accounts = False
            log_info = _("Error: More than one property account expense found.")
        return accounts, log_info

    def _create_product(self):
        self.ensure_one()
        product, log_info = self._check_product()
        if not product and not log_info:
            product_obj = self.env["product.product"]
            values = self._product_values()
            values.update({
                "name": self.product_name})
            product = product_obj.create(values)
            log_info = ""
        return product, log_info

    def _update_product(self):
        self.ensure_one()
        product = self.product_id
        values = self._product_values()
        product.write(values)
        log_info = ""
        return product, log_info

    def _product_values(self):
        self.ensure_one()
        values = {
            "default_code": self.product_default_code,
            "uom_id": self.product_uom_id.id,
            "uom_po_id": self.purchase_uom_id.id or self.product_uom_id.id,
            "sale_ok": self.sale_ok,
            "purchase_ok": self.purchase_ok,
            "list_price": self.list_price,
            "standard_price": self.standard_price,
            "invoice_policy": self.invoice_policy,
            "categ_id": self.category_id.id,
            "type": self.product_type,
            "purchase_method": self.purchase_method,
            "description_purchase": self.description_purchase,
            "property_account_income_id": self.property_account_income_id.id,
            "property_account_expense_id": self.property_account_expense_id.id,
            }
        if self.barcode:
            values.update({
                "barcode": self.barcode,
                })
        if self.customer_tax_id:
            values.update({
                "taxes_id": [(4, self.customer_tax_id.id)],
                })
        return values
