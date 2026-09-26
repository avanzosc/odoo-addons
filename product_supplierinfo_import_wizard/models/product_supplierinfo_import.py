# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import (
    check_number,
    convert2date,
)


class ProductSupplierinfoImport(models.Model):
    _name = "product.supplierinfo.import"
    _inherit = "base.import"

    import_line_ids = fields.One2many(
        comodel_name="product.supplierinfo.import.line",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
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
            product_name = row_values.get("Plantilla de producto", "")
            product_code = row_values.get("Código de producto", "")
            if not product_name and not product_code:
                return {}
            supplier_name = row_values.get("Proveedor", "")
            supplier_product_name = row_values.get(
                "Nombre del producto del proveedor", ""
            )
            supplier_product_code = row_values.get(
                "Código de producto del proveedor", ""
            )
            sequence = row_values.get("Secuencia", "")
            currency_code = row_values.get("Moneda", "")
            min_qty = row_values.get("Cantidad mínima", 0.0)
            date_start = row_values.get("Fecha de inicio", False)
            date_end = row_values.get("Fecha finalización", "")
            price = row_values.get("Precio", 0.0)
            delay = row_values.get("Tiempo inicial entrega", 1)
            values.update(
                {
                    "product_code": str(product_code),
                    "product_name": product_name or str(product_code),
                    "sequence": sequence,
                    "supplier_name": supplier_name,
                    "supplier_product_name": supplier_product_name,
                    "supplier_product_code": supplier_product_code,
                    "currency_code": currency_code,
                    "min_qty": check_number(min_qty),
                    "price": check_number(price),
                    "date_start": convert2date(date_start, datemode=datemode).date()
                    if date_start
                    else False,
                    "date_end": convert2date(date_end, datemode=datemode).date()
                    if date_end
                    else False,
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
    _inherit = "base.import.line"

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
        default=1,
        help="Assigns the priority to the list of product vendor.",
        copy=False,
    )
    product_code = fields.Char(
        copy=False,
    )
    product_name = fields.Char(
        string="Product",
        copy=False,
    )
    product_barcode = fields.Char(
        string="Barcode",
        help="International Article Number used for product identification.",
        copy=False,
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        copy=False,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        copy=False,
    )
    supplier_name = fields.Char(
        copy=False,
    )
    supplier_id = fields.Many2one(
        comodel_name="res.partner",
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
        copy=False,
    )
    min_qty = fields.Float(
        string="Minimal Quantity",
        help="The minimal quantity to purchase from this vendor, expressed in the "
        "vendor Product Unit of Measure if not any, in the default unit of "
        "measure of the product otherwise.",
        copy=False,
    )
    currency_code = fields.Char(
        string="Currency",
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
        copy=False,
    )
    product_supplierinfo_id = fields.Many2one(
        comodel_name="product.supplierinfo",
        readonly=True,
        copy=False,
    )

    @api.onchange("product_tmpl_id")
    def onchange_product_tmpl_id(self):
        for record in self:
            record.product_name = record.product_tmpl_id.name
            record.product_code = record.product_tmpl_id.default_code

    @api.onchange("supplier_id")
    def onchange_supplier_id(self):
        for record in self:
            record.supplier_name = record.supplier_id.name

    def _check_supplier(self):
        self.ensure_one()
        log_info = ""
        partner_obj = self.env["res.partner"].with_context(
            force_company_id=self.import_id.company_id.id
        )
        if self.supplier_id:
            return self.supplier_id, log_info
        search_domain = [
            ("name", "=", self.supplier_name),
            ("parent_id", "=", False),
        ]
        # field_domain = self._domain_supplier_id()
        # if field_domain:
        #     search_domain = expression.AND(
        #         [
        #             search_domain,
        #             field_domain,
        #         ]
        #     )
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
        product_obj = self.env["product.template"].with_context(
            force_company_id=self.import_id.company_id.id
        )
        if self.product_tmpl_id:
            return self.product_tmpl_id, log_info
        if self.product_barcode:
            search_domain = [
                ("barcode", "=", self.product_barcode),
            ]
        else:
            search_domain = [
                ("default_code", "=", self.product_code),
            ]
        products = product_obj.search(search_domain)
        name_domain = [
            ("name", "=", self.product_name),
        ]
        if not products:
            search_domain = expression.OR([search_domain, name_domain])
        elif len(products) > 1:
            search_domain = expression.OR(
                [
                    search_domain,
                    name_domain,
                ]
            )
        # search_domain = expression.AND(
        #     [
        #         [
        #             "|",
        #             ("company_id", "=", self.import_id.company_id.id),
        #             ("company_id", "=", False),
        #         ],
        #         search_domain,
        #     ]
        # )
        products = product_obj.search(search_domain)
        if not products:
            log_info = _("No product found.")
        elif len(products) > 1:
            products = False
            log_info = _("More than one product already exist.")
        return products and products[:1], log_info

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
            "min_qty": self.min_qty,
            "price": self.price,
            "currency_id": self.currency_id.id,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "delay": self.delay,
        }
