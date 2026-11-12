# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re

from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import (
    check_number,
    convert2date,
    convert2str,
)


class ProductSupplierinfoImport(models.Model):
    _name = "product.supplierinfo.import"
    _description = "Import Wizard for Supplier Pricelist"
    _inherit = "base.import"

    import_line_ids = fields.One2many(
        comodel_name="product.supplierinfo.import.line",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
        copy=False,
    )
    supplierinfo_count = fields.Integer(
        compute="_compute_supplierinfo_count",
    )

    def _compute_supplierinfo_count(self):
        for record in self:
            record.supplierinfo_count = len(
                record.mapped("import_line_ids.product_supplierinfo_id")
            )

    def _get_line_values(self, row_values=False, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values, datemode=datemode)
        if row_values:
            log_infos = []
            product_name = self._get_row_value(
                row_values, _("Product Template"), "Product Template", ""
            )
            product_code = self._get_row_value(
                row_values, _("Internal Reference"), "Internal Reference", ""
            )

            if not product_name and not product_code:
                return {}

            product_barcode = self._get_row_value(
                row_values, _("Barcode"), "Barcode", ""
            )

            supplier_name = self._get_row_value(row_values, _("Vendor"), "Vendor", "")
            supplier_product_name = self._get_row_value(
                row_values, _("Vendor Product Name"), "Vendor Product Name", ""
            )
            supplier_product_code = self._get_row_value(
                row_values, _("Vendor Product Code"), "Vendor Product Code", ""
            )

            date_start = self._get_row_value(
                row_values, _("Start Date"), "Start Date", False
            )
            date_end = self._get_row_value(row_values, _("End Date"), "End Date", False)

            sequence = self._get_row_value(row_values, _("Sequence"), "Sequence", "")
            currency_code = self._get_row_value(
                row_values, _("Currency"), "Currency", ""
            )
            min_qty = self._get_row_value(row_values, _("Quantity"), "Quantity", 0.0)
            price = self._get_row_value(row_values, _("Price"), "Price", False)
            delay = self._get_row_value(
                row_values, _("Delivery Lead Time"), "Delivery Lead Time", False
            )
            values.update(
                {
                    "product_code": convert2str(product_code),
                    "product_name": product_name or convert2str(product_code),
                    "product_barcode": convert2str(product_barcode),
                    "sequence": sequence,
                    "supplier_name": convert2str(supplier_name),
                    "supplier_product_name": convert2str(supplier_product_name),
                    "supplier_product_code": convert2str(supplier_product_code),
                    "currency_code": currency_code,
                    "min_qty": check_number(min_qty),
                    "date_start": convert2date(date_start, datemode=datemode).date()
                    if date_start
                    else False,
                    "date_end": convert2date(date_end, datemode=datemode).date()
                    if date_end
                    else False,
                }
            )
            if price:
                values.update(
                    {
                        "price": check_number(price),
                    }
                )
            if delay:
                values.update(
                    {
                        "delay": check_number(delay),
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

    def button_open_import_line(self):
        action = super().button_open_import_line()
        action["context"].update({"import_hide": False})
        return action

    def button_open_supplierinfo(self):
        self.ensure_one()
        supplierinfos = self.mapped("import_line_ids.product_supplierinfo_id")
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "product.product_supplierinfo_type_action"
        )
        action["domain"] = expression.AND(
            [[("id", "in", supplierinfos.ids)], safe_eval(action.get("domain") or "[]")]
        )
        return action


class ProductSupplierinfoImportLine(models.Model):
    _name = "product.supplierinfo.import.line"
    _description = "Import Wizard Line for Supplier Pricelist"
    _inherit = "base.import.line"

    def _default_sequence(self):
        default_dict = self.env["product.supplierinfo"].default_get(["sequence"])
        return default_dict.get("sequence")

    def _default_min_qty(self):
        default_dict = self.env["product.supplierinfo"].default_get(["min_qty"])
        return default_dict.get("min_qty")

    def _default_price(self):
        default_dict = self.env["product.supplierinfo"].default_get(["price"])
        return default_dict.get("price")

    def _default_delay(self):
        default_dict = self.env["product.supplierinfo"].default_get(["delay"])
        return default_dict.get("delay")

    import_id = fields.Many2one(
        comodel_name="product.supplierinfo.import",
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        ondelete={"create": "set default"},
        copy=False,
    )
    sequence = fields.Integer(
        default=_default_sequence,
        help="Assigns the priority to the list of product vendor.",
        copy=False,
    )
    product_code = fields.Char(
        copy=False,
    )
    product_name = fields.Char(
        copy=False,
    )
    product_barcode = fields.Char(
        string="Barcode",
        help="International Article Number used for product identification.",
        copy=False,
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
        check_company=True,
        ondelete="cascade",
        copy=False,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product Variant",
        check_company=True,
        domain="[('product_tmpl_id', '=', product_tmpl_id)] if product_tmpl_id else []",
        help="If not set, the vendor price will apply to all variants of this product.",
        copy=False,
    )
    supplier_name = fields.Char(
        copy=False,
    )
    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Vendor",
        ondelete="cascade",
        check_company=True,
        copy=False,
    )
    supplier_product_name = fields.Char(
        string="Vendor Product Name",
        help="This vendor's product name will be used when printing a request for "
        "quotation. Keep empty to use the internal one.",
        copy=False,
    )
    supplier_product_code = fields.Char(
        string="Vendor Product Code",
        help="This vendor's product code will be used when printing a request for "
        "quotation. Keep empty to use the internal one.",
        copy=False,
    )
    price = fields.Float(
        digits="Product Price",
        help="The price to purchase a product",
        default=_default_price,
        copy=False,
    )
    discount = fields.Float(
        string="Discount (%)",
        digits="Discount",
    )
    min_qty = fields.Float(
        string="Quantity",
        help="The minimal quantity to purchase from this vendor, expressed in the "
        "vendor Product Unit of Measure if not any, in the default unit of "
        "measure of the product otherwise.",
        digits="Product Unit of Measure",
        default=_default_min_qty,
        copy=False,
    )
    currency_code = fields.Char(
        default=lambda self: self.env.company.currency_id.name,
        copy=False,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        copy=False,
    )
    date_start = fields.Date(
        string="Start Date",
        help="Start date for this vendor price",
        copy=False,
    )
    date_end = fields.Date(
        string="End Date",
        help="End date for this vendor price",
        copy=False,
    )
    delay = fields.Integer(
        string="Delivery Lead Time",
        help="Lead time in days between the confirmation of the purchase order and the "
        "receipt of the products in your warehouse. Used by the scheduler for "
        "automatic computation of the purchase order planning.",
        default=_default_delay,
        copy=False,
    )
    product_supplierinfo_id = fields.Many2one(
        comodel_name="product.supplierinfo",
        readonly=True,
        copy=False,
    )
    company_id = fields.Many2one(
        related="import_id.company_id",
    )

    @api.onchange("product_tmpl_id")
    def onchange_product_tmpl_id(self):
        for record in self:
            record.product_name = record.product_tmpl_id.name
            record.product_code = record.product_tmpl_id.default_code
            record.product_barcode = record.product_tmpl_id.barcode

    @api.onchange("product_id")
    def onchange_product_id(self):
        for record in self:
            record.product_tmpl_id = record.product_id.product_tmpl_id
            record.product_name = record.product_id.name
            record.product_code = record.product_id.default_code
            record.product_barcode = record.product_id.barcode

    @api.onchange("supplier_id")
    def onchange_supplier_id(self):
        for record in self:
            record.supplier_name = record.supplier_id.name

    def _get_supplier_domain(self):
        self.ensure_one()
        return [
            ("name", "=ilike", (self.supplier_name or "").strip()),
            ("parent_id", "=", False),
            ("supplier_rank", ">", 0),
        ]

    def _get_product_domain(self):
        self.ensure_one()
        return []

    def _check_supplier(self):
        self.ensure_one()
        log_info = ""
        partner_obj = self.env["res.partner"].with_company(self.import_id.company_id.id)
        if self.supplier_id and self.supplier_id.exists():
            return self.supplier_id, log_info
        if not (self.supplier_name or "").strip():
            log_info = _("No supplier name provided.")
            return False, log_info
        search_domain = expression.AND(
            [
                [
                    ("company_id", "in", (self.import_id.company_id.id, False)),
                ],
                self._get_supplier_domain(),
            ]
        )
        suppliers = partner_obj.search(search_domain)
        if not suppliers:
            log_info = _("No supplier found with name {}.").format(self.supplier_name)
        elif len(suppliers) > 1:
            suppliers = False
            log_info = _("More than one supplier with name {} already exist.").format(
                self.supplier_name
            )
        return suppliers and suppliers[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        product_obj = self.env["product.product"].with_company(
            self.import_id.company_id.id
        )
        if self.product_tmpl_id and self.product_tmpl_id.exists():
            return self.product_tmpl_id, log_info

        product_name = (self.product_name or "").strip()
        product_code = (self.product_code or "").strip()
        name_match = re.search(r"\[(.*?)\]", product_name)
        if not product_code and name_match:
            product_code = name_match.group(1).strip()
        if name_match:
            product_name = product_name[name_match.end() :].strip()

        company_domain = [
            ("company_id", "in", (self.import_id.company_id.id, False)),
        ]
        products = product_obj.browse()
        if self.product_barcode:
            products = product_obj.search(
                expression.AND(
                    [company_domain, [("barcode", "=", self.product_barcode)]]
                )
            )
        if not products and product_code:
            products = product_obj.search(
                expression.AND([company_domain, [("default_code", "=", product_code)]])
            )
        if not products and product_name:
            products = product_obj.search(
                expression.AND([company_domain, [("name", "=ilike", product_name)]])
            )
        if len(products) > 1 and product_name:
            matching_products = products.filtered(
                lambda p: (p.name or "").strip().lower() == product_name.lower()
            )
            products = matching_products or products
        templates = products.product_tmpl_id
        if not products:
            log_info = _("No product found.")
        elif len(templates) > 1:
            templates = self.env["product.template"].browse()
            log_info = _("More than one product already exist.")
        return templates[:1], log_info

    def _check_currency(self):
        self.ensure_one()
        log_info = ""
        currency_obj = self.env["res.currency"].with_context(active_test=False)
        if self.currency_id:
            return self.currency_id, log_info
        search_domain = [
            ("name", "=", self.currency_code),
        ]
        currencies = currency_obj.search(search_domain)
        if not currencies:
            log_info = _("No currency found with code '{}'.").format(self.currency_code)
        elif not currencies[:1].active:
            log_info = _("'{}' is inactive.").format(self.currency_code)
        return currencies and currencies[:1], log_info

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        supplier, log_info_supplier = self._check_supplier()
        if log_info_supplier:
            log_infos.append(log_info_supplier)
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        currency, log_info_currency = self._check_currency()
        if log_info_currency:
            log_infos.append(log_info_currency)
        state = "error" if log_infos else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "supplier_id": supplier and supplier.id,
                "product_tmpl_id": product and product.id,
                "product_code": product and product.default_code,
                "product_barcode": product and product.barcode,
                "currency_id": currency and currency.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        supplierinfo = self.env["product.supplierinfo"].create(
            self._product_supplierinfo_values()
        )
        update_values.update(
            {
                "product_supplierinfo_id": supplierinfo and supplierinfo.id,
                "log_info": "",
                "state": "done",
            }
        )
        return update_values

    def _product_supplierinfo_values(self):
        self.ensure_one()
        return {
            "sequence": self.sequence,
            "partner_id": self.supplier_id.id,
            "product_tmpl_id": self.product_tmpl_id.id,
            "product_id": self.product_id.id,
            "product_name": self.supplier_product_name,
            "product_code": self.supplier_product_code,
            "min_qty": self.min_qty,
            "price": self.price,
            "discount": self.discount,
            "currency_id": self.currency_id.id,
            "company_id": self.import_id.company_id.id,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "delay": self.delay,
        }
