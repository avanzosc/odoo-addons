# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp


class ProductImport(models.Model):
    _name = "product.cost.import"
    _inherit = "base.import"
    _description = "Wizard to import products' costs"

    import_line_ids = fields.One2many(
        comodel_name="product.cost.import.line",
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
            "product.import"
        ),
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

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            log_infos = []
            product_code = row_values.get("Product Code", "")
            product_name = row_values.get("Product Name", "")
            if not product_name and not product_code:
                return {}
            standard_price = row_values.get("Standard Price", "")
            values.update(
                {
                    "product_name": product_name or str(product_code),
                    "product_default_code": product_code,
                    "standard_price": standard_price,
                }
            )
            if not product_name:
                log_infos.append(_("Product Code added as Product Name"))
            values.update(
                {
                    "log_info": "\n".join(log_infos),
                    "state": "error" if log_infos else "2validate",
                }
            )
        return values

    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.mapped("import_line_ids.product_id"))

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
    _name = "product.cost.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import products' costs"

    import_id = fields.Many2one(
        comodel_name="product.cost.import",
    )
    action = fields.Selection(
        selection_add=[
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
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    standard_price = fields.Float(
        string="Cost",
        digits=dp.get_precision('Product Price'),
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_old_price = fields.Float(
        string="Old Cost",
        digits=dp.get_precision('Product Price'),
        readonly=True,
        copy=False,
    )
    product_standard_price = fields.Float(
        string="Actual Cost",
        digits=dp.get_precision('Product Price'),
        readonly=True,
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        state = "error" if log_infos else "pass"
        action = "nothing" if state == "error" else "update"
        update_values.update(
            {
                "product_id": product and product.id,
                "product_old_price": product and product.standard_price or 0.0,
                "product_standard_price": product and product.standard_price or 0.0,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        if self.action == "update":
            product, log_info = self._update_product()
            state = "error" if log_info else "done"
            update_values.update(
                {
                    "product_standard_price": product and product.standard_price or self.product_standard_price,
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
            else:
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
        if not products:
            log_info = _("Product not found.")
        elif len(products) > 1:
            products = False
            log_info = _("More than one product already exist.")
        return products, log_info

    def _update_product(self):
        self.ensure_one()
        self.product_id.with_context(force_company=self.import_id.company_id.id).write(self._product_values())
        return self.product_id, ""

    def _product_values(self):
        self.ensure_one()
        values = {
            "standard_price": self.standard_price,
        }
        return values
