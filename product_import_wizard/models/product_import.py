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
        states={"done": [("readonly", True)]},
        copy=False,
    )
    uom_id = fields.Many2one(
        string="Default Unit of Measure",
        comodel_name="uom.uom",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_count = fields.Integer(
        string="Products",
        compute="_compute_product_count",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env["res.company"]._company_default_get(
            "product.import"),
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_found_reference = fields.Boolean(
        string="Found Product Only By Internal Reference",
        default=False,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    data = fields.Binary(
        required=False,
        states={"done": [("readonly", True)]},
        copy=False,
    )

    @api.onchange("uom_id")
    def _onchange_uom_id(self):
        if self.uom_id:
            for line in self.import_line_ids.filtered(
                lambda c: not c.product_uom and (not c.product_uom_id)
            ):
                line.product_uom = self.uom_id.name
                line.product_uom_id = self.uom_id.id

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            log_infos = []
            product_code = row_values.get("Product Code", "")
            product_name = row_values.get("Product Name", "")
            if not product_name and not product_code:
                return {}
            import_line_obj = self.env["product.import.line"]
            sale_ok = bool(row_values.get(
                "Sale OK", import_line_obj.default_sale_ok()))
            purchase_ok = bool(
                row_values.get(
                    "Purchase OK", import_line_obj.default_purchase_ok())
            )
            product_type = self.product_type or row_values.get(
                "Product Type", "")
            category_name = row_values.get("Category Name", "")
            barcode = row_values.get("Barcode", "")
            list_price = row_values.get("List Price", "")
            customer_tax = row_values.get("Customer Tax", "")
            standard_price = row_values.get("Standard Price", "")
            uom_name = row_values.get("UoM Name", self.uom_id.name)
            purchase_uom_name = row_values.get("Purchase UoM Name", "")
            invoice_policy = row_values.get("Invoice Policy", "")
            purchase_method = row_values.get("Purchase Method", "")
            description_purchase = row_values.get("Description Purchase", "")
            property_account_income = row_values.get(
                "Property Account Income", "")
            property_account_expense = row_values.get(
                "Property Account Expense", "")
            values.update(
                {
                    "product_name": product_name or str(product_code),
                    "sale_ok": sale_ok,
                    "purchase_ok": purchase_ok,
                    "product_default_code": product_code,
                    "category_name": category_name,
                    "barcode": barcode,
                    "list_price": list_price,
                    "customer_tax": customer_tax,
                    "standard_price": standard_price,
                    "product_uom": uom_name,
                    "purchase_uom_name": purchase_uom_name,
                    "description_purchase": description_purchase,
                    "property_account_income": property_account_income,
                    "property_account_expense": property_account_expense,
                }
            )
            if not product_name:
                log_infos.append(_("Product Code added as Product Name"))
            if product_type:
                l = [w for w, v in import_line_obj._get_selection_product_type(
                    )]
                if product_type not in l:
                    log_infos.append(_("Product Type not understood."))
                else:
                    values.update(
                        {
                            "product_type": product_type,
                        }
                    )
            if purchase_method:
                if (
                    purchase_method
                    not in import_line_obj._get_selection_purchase_method()
                ):
                    log_infos.append(_("Purchase Method not understood."))
                else:
                    values.update(
                        {
                            "product_type": purchase_method,
                        }
                    )
            if invoice_policy:
                if (
                    invoice_policy
                    not in import_line_obj._get_selection_invoice_policy()
                ):
                    log_infos.append(_("Invoice Policy not understood"))
                else:
                    values.update(
                        {
                            "invoice_policy": invoice_policy,
                        }
                    )
            if not uom_name and self.uom_id:
                values.update(
                    {
                        "product_uom": self.uom_id.name,
                        "product_uom_id": self.uom_id.id,
                    }
                )
            values.update(
                {
                    "log_info": "\n".join(log_infos),
                    "state": "error" if log_infos else "2validate",
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
        return self.env["product.product"].fields_get(allfields=[
            "purchase_method"])["purchase_method"]["selection"]

    @api.model
    def _get_selection_invoice_policy(self):
        return self.env["product.product"].fields_get(allfields=[
            "invoice_policy"])["invoice_policy"]["selection"]

    def default_product_type(self):
        default_dict = self.env["product.product"].default_get(["type"])
        return default_dict.get("type")

    def default_sale_ok(self):
        default_dict = self.env["product.product"].default_get(["sale_ok"])
        return default_dict.get("sale_ok")

    def default_purchase_ok(self):
        default_dict = self.env["product.product"].default_get(
            ["purchase_ok"])
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
        selection_add=[
            ("create", "Create"),
            ("update", "Update"),
        ],
        ondelete="cascade",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_name = fields.Char(
        required=True,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_default_code = fields.Char(
        string="Internal Reference",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    barcode = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_type = fields.Selection(
        selection="_get_selection_product_type",
        default=default_product_type,
        required=True,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_uom = fields.Char(
        string="Product UoM",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_uom_id = fields.Many2one(
        string="Unit of Measure",
        comodel_name="uom.uom",
        domain="[('name','ilike',product_uom)]",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    category_name = fields.Char(
        string="Product Category Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        domain="[('name','ilike',category_name)]",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_ok = fields.Boolean(
        string="Can be Sold",
        default=default_sale_ok,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_ok = fields.Boolean(
        string="Can be Purchased",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    list_price = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    customer_tax = fields.Char(
        string="Customer Tax Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    standard_price = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_uom_name = fields.Char(
        string="Purchase UoM Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    invoice_policy = fields.Selection(
        selection="_get_selection_invoice_policy",
        default=default_invoice_policy,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_uom_id = fields.Many2one(
        string="Purchase UoM",
        comodel_name="uom.uom",
        domain="[('name','ilike',purchase_uom_name)]",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    customer_tax_id = fields.Many2one(
        string="Customer Tax",
        comodel_name="account.tax",
        domain="[('name','ilike',customer_tax)]",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_method = fields.Selection(
        selection="_get_selection_purchase_method",
        default=default_purchase_method,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    description_purchase = fields.Text(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    property_account_income = fields.Char(
        string="Income Account Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    property_account_income_id = fields.Many2one(
        string="Income Account",
        comodel_name="account.account",
        domain=[('deprecated', '=', False)],
        states={"done": [("readonly", True)]},
        copy=False,
    )
    property_account_expense = fields.Char(
        string="Expense Account Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    property_account_expense_id = fields.Many2one(
        string="Expense Account",
        comodel_name="account.account",
        domain=[('deprecated', '=', False)],
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        tax = purchase_uom = account_income = account_expense = False
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        category, log_info_category = self._check_category(product=product)
        if log_info_category:
            log_infos.append(log_info_category)
        uom, log_info_uom = self._check_sale_uom(product=product)
        if log_info_uom:
            log_infos.append(log_info_uom)
        if self.purchase_uom_name:
            purchase_uom, log_info_purchase_uom = self._check_purchase_uom()
            if log_info_purchase_uom:
                log_infos.append(log_info_purchase_uom)
        if self.customer_tax:
            tax, log_info_tax = self._check_tax()
            if log_info_tax:
                log_infos.append(log_info_tax)
        if self.barcode:
            log_info_barcode = self._check_barcode()
            if log_info_barcode:
                log_infos.append(log_info_barcode)
        if self.property_account_income:
            account_income, log_info_income = self._check_account_income()
            if log_info_income:
                log_infos.append(log_info_income)
        if self.property_account_expense:
            account_expense, log_info_expense = self._check_account_expense()
            if log_info_expense:
                log_infos.append(log_info_expense)
        state = "error" if log_infos else "pass"
        action = "nothing"
        if product and state != "error":
            action = "update"
        elif state != "error":
            action = "create"
        update_values.update(
            {
                "product_id": product and product.id,
                "category_id": category and category.id,
                "product_uom_id": uom and uom.id,
                "purchase_uom_id": purchase_uom and purchase_uom.id,
                "customer_tax_id": tax and tax.id,
                "property_account_income_id": account_income and (
                    account_income.id),
                "property_account_expense_id": account_expense and (
                    account_expense.id),
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        if self.action == "create":
            product, log_info = self._create_product()
        elif self.action == "update":
            product, log_info = self._update_product()
        state = "error" if log_info else "done"
        update_values.update(
            {
                "product_id": product and product.id,
                "log_info": log_info,
                "state": state,
            }
        )
        return update_values

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.product_id:
            return self.product_id, log_info
        product_obj = self.env["product.product"]
        search_domain = [("name", "=", self.product_name)]
        if self.product_default_code:
            if self.import_id.product_found_reference:
                search_domain = [("default_code", "=", self.product_default_code)]
            search_domain = expression.AND(
                [[("default_code", "=", self.product_default_code)], search_domain]
            )
        search_domain = expression.AND(
            [
                [
                    "|",
                    ("company_id", "=", self.import_id.company_id.id),
                    ("company_id", "=", False),
                ],
                search_domain,
            ]
        )
        products = product_obj.search(search_domain)
        if len(products) > 1:
            products = False
            log_info = _("More than one product already exist.")
        return products, log_info

    def _check_category(self, product=False):
        self.ensure_one()
        log_info = ""
        if self.category_id:
            return self.category_id, log_info
        category_obj = self.env["product.category"]
        search_domain = [("name", "=", self.category_name)]
        if product and not self.category_name:
            return product.categ_id, log_info
        categories = category_obj.search(search_domain)
        if not categories:
            categories = False
            log_info = (
                _("Product category named %(category_name)s not found.") % {
                    "category_name": self.category_name,})
        elif len(categories) > 1:
            categories = False
            log_info = _("More than one product category exist.")
        return categories, log_info

    def _check_sale_uom(self, product=False):
        self.ensure_one()
        log_info = ""
        if self.product_uom_id:
            return self.product_uom_id, log_info
        if product and not self.product_uom:
            return product.uom_id, log_info
        return self._check_uom(self.product_uom)

    def _check_purchase_uom(self):
        self.ensure_one()
        log_info = ""
        if self.purchase_uom_id:
            return self.purchase_uom_id, log_info
        return self._check_uom(self.purchase_uom_name)

    def _check_uom(self, uom_name=False):
        self.ensure_one()
        log_info = ""
        uom_obj = self.env["uom.uom"]
        search_domain = [("name", "ilike", uom_name)]
        uoms = uom_obj.search(search_domain)
        if not uoms:
            log_info = _("Unit of measure not found.")
        elif len(uoms) > 1:
            uoms = False
            log_info = _("More than one unit of measure exist.")
        return uoms and uoms[:1], log_info

    def _check_tax(self):
        self.ensure_one()
        log_info = ""
        if self.customer_tax_id:
            return self.customer_tax_id, log_info
        if not self.customer_tax:
            return False, log_info
        tax_obj = self.env["account.tax"]
        search_domain = [
            "&",
            ("name", "ilike", self.customer_tax),
            "|",
            ("company_id", "=", self.import_id.company_id.id),
            ("company_id", "=", False),
        ]
        taxes = tax_obj.search(search_domain)
        if not taxes:
            log_info = _("Tax not found.")
        elif len(taxes) > 1:
            taxes = False
            log_info = _("More than one taxes found.")
        return taxes and taxes[:1], log_info

    def _check_barcode(self):
        self.ensure_one()
        log_info = ""
        if self.barcode:
            same_barcode = self.import_id.import_line_ids.filtered(
                lambda c: c.barcode == self.barcode and c.id != self.id
            )
            if same_barcode:
                log_info = _(
                    "There are other lines in this importer with the same" +
                    " barcode.")
            same_barcode = self.env["product.product"].search(
                [
                    ("name", "!=", self.product_name),
                    ("barcode", "=", self.barcode)]
            )
            if same_barcode:
                log_info = _(
                    "Another product with the same barcode exists in" +
                    " the system.")
            return log_info

    def _check_account_income(self):
        self.ensure_one()
        log_info = ""
        if self.property_account_income_id:
            return self.property_account_income_id, log_info
        account_obj = self.env["account.account"]
        search_domain = [
            ("code", "=", self.property_account_income),
        ]
        search_domain = expression.AND(
            [
                safe_eval(
                    [('deprecated', '=', False)], {
                        "current_company_id": self.import_id.company_id.id}
                ),
                search_domain,
            ]
        )
        accounts = account_obj.search(search_domain)
        if not accounts:
            log_info = _("Property account income not found.")
        elif len(accounts) > 1:
            accounts = False
            log_info = _("More than one property account income found.")
        return accounts and accounts[:1], log_info

    def _check_account_expense(self):
        self.ensure_one()
        log_info = ""
        if self.property_account_expense_id:
            return self.property_account_expense_id, log_info
        account_obj = self.env["account.account"]
        search_domain = [
            ("code", "=", self.property_account_expense),
        ]
        search_domain = expression.AND(
            [
                safe_eval(
                    [('deprecated', '=', False)],
                    {"current_company_id": self.import_id.company_id.id}
                ),
                search_domain,
            ]
        )
        accounts = account_obj.search(search_domain)
        if not accounts:
            log_info = _("Property account expense not found.")
        elif len(accounts) > 1:
            accounts = False
            log_info = _("More than one property account expense found.")
        return accounts and accounts[:1], log_info

    def _create_product(self):
        self.ensure_one()
        product, log_info = self._check_product()
        if not product and not log_info:
            product_obj = self.env["product.product"]
            values = self._product_values()
            values.update(
                {
                    "name": self.product_name,
                    "company_id": self.import_id.company_id.id,
                }
            )
            product = product_obj.create(values)
            log_info = ""
        return product, log_info

    def _update_product(self):
        self.ensure_one()
        self.product_id.write(
            self._product_values()
        )
        return self.product_id, ""

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
            values.update(
                {
                    "barcode": self.barcode,
                }
            )
        if self.customer_tax_id:
            values.update(
                {
                    "taxes_id": [(4, self.customer_tax_id.id)],
                }
            )
        return values
