# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import unicodedata

from odoo import _, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import convert2date, convert2str


class PurchaseOrderImport(models.Model):
    _name = "purchase.order.import"
    _inherit = "base.import"
    _description = "Wizard to import purchase orders"

    import_line_ids = fields.One2many(
        comodel_name="purchase.order.import.line",
    )
    purchase_order_count = fields.Integer(
        string="# Purchase Orders",
        compute="_compute_purchase_order_count",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company.id,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        timezone = self._context.get("tz") or "UTC"
        if row_values:
            purchase_origin = row_values.get("Entrada", "")
            if not purchase_origin:
                return {}
            purchase_supplier_code = row_values.get("CodigoProveedor", "")
            purchase_supplier_name = row_values.get("NombreProveedor", "")
            purchase_create_date = row_values.get("Fecha", "")
            purchase_date_confirm = row_values.get("FechaConfirmada", "")
            purchase_product_code = row_values.get("CodigoProducto", "")
            purchase_product_name = row_values.get("NombreProducto", "")
            purchase_ordered_qty = row_values.get("KgProveedor", "")
            purchase_qty_done = row_values.get("KgNeto", "")
            purchase_price_unit = row_values.get("PrecioUnitario", "")
            purchase_discount = row_values.get("Descuento", "")
            purchase_state = row_values.get("Estado", "")
            purchase_warehouse = row_values.get("CodigoAlmacen", "")
            log_info = ""
            values.update(
                {
                    "purchase_supplier_code": convert2str(purchase_supplier_code),
                    "purchase_supplier_name": purchase_supplier_name.title(),
                    "purchase_create_date": convert2date(
                        purchase_create_date, datemode=datemode, timezone_name=timezone
                    ),
                    "purchase_date_confirm": convert2date(
                        purchase_date_confirm, datemode=datemode, timezone_name=timezone
                    ),
                    "purchase_origin": convert2str(purchase_origin),
                    "purchase_product_code": convert2str(purchase_product_code),
                    "purchase_product_name": convert2str(purchase_product_name),
                    "purchase_ordered_qty": purchase_ordered_qty,
                    "purchase_qty_done": purchase_qty_done,
                    "purchase_price_unit": purchase_price_unit,
                    "purchase_discount": purchase_discount,
                    "purchase_state": convert2str(purchase_state),
                    "purchase_warehouse": convert2str(purchase_warehouse),
                    "log_info": log_info,
                }
            )
        return values

    def _compute_purchase_order_count(self):
        for record in self:
            record.purchase_order_count = len(
                record.mapped("import_line_ids.purchase_order_id")
            )

    def button_open_purchase_order(self):
        self.ensure_one()
        orders = self.mapped("import_line_ids.purchase_order_id")
        action = self.env.ref("purchase.purchase_form_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", orders.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class PurchaseOrderImportLine(models.Model):
    _name = "purchase.order.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import purchase orders"

    import_id = fields.Many2one(
        comodel_name="purchase.order.import",
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        ondelete={"create": "set default"},
    )
    purchase_order_id = fields.Many2one(
        string="Purchase Order",
        comodel_name="purchase.order",
    )
    purchase_supplier_code = fields.Char(
        string="Supplier Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_supplier_name = fields.Char(
        string="Supplier Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_create_date = fields.Datetime(
        string="CreateDate",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_date_confirm = fields.Datetime(
        string="DateConfirm",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_origin = fields.Char(
        string="Partner Ref",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_product_name = fields.Char(
        string="Product Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_ordered_qty = fields.Float(
        string="Ordered Qty",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_qty_done = fields.Float(
        string="Qty Done",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_price_unit = fields.Float(
        string="Price Unit",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_discount = fields.Float(
        string="Discount",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_state = fields.Char(
        string="State",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_warehouse = fields.Char(
        string="Warehouse",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_supplier_id = fields.Many2one(
        string="Supplier",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        string="Warehouse",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Picking Type",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        picking_type = False
        if self.purchase_origin:
            origin, log_info = self._check_origin()
            if log_info:
                update_values.update(
                    {
                        "log_info": log_info,
                        "state": "error",
                        "action": "nothing",
                    }
                )
                return update_values
        supplier, log_info_supplier = self._check_supplier()
        if log_info_supplier:
            log_infos.append(log_info_supplier)
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        warehouse, log_info_warehouse = self._check_warehouse()
        if log_info_warehouse:
            log_infos.append(log_info_warehouse)
        if warehouse:
            picking_type, log_info_picking_type = self._check_picking_type(
                warehouse=warehouse
            )
            if log_info_picking_type:
                log_infos.append(log_info_picking_type)
        state = "error" if log_infos else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "purchase_supplier_id": supplier and supplier.id,
                "purchase_product_id": product and product.id,
                "purchase_warehouse_id": warehouse and warehouse.id,
                "purchase_picking_type_id": (picking_type and picking_type.id),
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        if self.action != "nothing":
            log_infos = []
            if self.action == "create":
                if not self.purchase_origin:
                    purchase = self._create_purchase_order()
                    self._create_purchase_order_line(purchase)
        state = "error" if log_infos else "done"
        update_values.append(
            {
                "purchase_order_id": purchase.id,
                "log_info": "\n".join(log_infos),
                "state": state,
            }
        )
        return update_values

    def _check_origin(self):
        self.ensure_one()
        purchase_obj = self.env["purchase.order"]
        search_domain = [("partner_ref", "=", self.purchase_origin)]
        log_info = ""
        purchases = purchase_obj.search(search_domain)
        if purchases:
            log_info = _("Error: Previously uploaded order.")
        return self.purchase_origin, log_info

    def _check_supplier(self):
        self.ensure_one()
        log_info = ""
        if self.purchase_supplier_id:
            return self.purchase_supplier_id, log_info
        supplier_obj = self.env["res.partner"]
        if self.purchase_supplier_code and not self.purchase_supplier_name:
            search_domain = [("ref", "=", self.purchase_supplier_code)]
        elif self.purchase_supplier_name and not self.purchase_supplier_code:
            search_domain = [("name", "=ilike", self.purchase_supplier_name)]
        elif self.purchase_supplier_code and self.purchase_supplier_name:
            search_domain = [
                "|",
                ("name", "=ilike", self.purchase_supplier_name),
                ("ref", "=", self.purchase_supplier_code),
            ]
        suppliers = supplier_obj.search(search_domain)
        if not suppliers:
            suppliers = False
            log_info = _("Error: No supplier found.")
        elif len(suppliers) > 1:
            if self.purchase_supplier_code and self.purchase_supplier_name:
                search_domain = [
                    ("name", "=ilike", self.purchase_supplier_name),
                    ("ref", "=", self.purchase_supplier_code),
                ]
                suppliers = supplier_obj.search(search_domain)
                if not len(suppliers) == 1:
                    suppliers = False
                    log_info = _("Error: More than one supplier found.")
        return suppliers and suppliers[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.purchase_product_id:
            return self.purchase_product_id, log_info
        product_obj = self.env["product.product"]
        if self.purchase_product_name:
            name = self.purchase_product_name.replace(" ", "")
            name = "".join(
                c
                for c in unicodedata.normalize("NFD", name)
                if unicodedata.category(c) != "Mn"
            )
        if self.purchase_product_code and not self.purchase_product_name:
            search_domain = [("default_code", "=", self.purchase_product_code)]
        elif self.purchase_product_name and not self.purchase_product_code:
            search_domain = [("trim_name", "=ilike", name)]
        elif self.purchase_product_code and self.purchase_product_name:
            search_domain = [
                "|",
                ("trim_name", "=ilike", name),
                ("default_code", "=", self.purchase_product_code),
            ]
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
            if self.purchase_product_code and self.purchase_product_name:
                search_domain = [
                    ("trim_name", "=ilike", name),
                    ("default_code", "=", self.purchase_product_code),
                ]
                products = product_obj.search(search_domain)
                if not len(products) == 1:
                    products = False
                    log_info = _(
                        "Error: More than one product with the same name or "
                        + "code found."
                    ).format(self.purchase_product_name, self.purchase_product_code)
        return products and products[:1], log_info

    def _check_warehouse(self):
        self.ensure_one()
        log_info = ""
        if self.import_id.warehouse_id:
            self.purchase_warehouse_id = self.import_id.warehouse_id.id
        if self.purchase_warehouse_id:
            return self.purchase_warehouse_id, log_info
        warehouse_obj = self.env["stock.warehouse"]
        search_domain = [
            "|",
            ("name", "=", self.purchase_warehouse),
            ("code", "=", self.purchase_warehouse),
        ]
        warehouses = warehouse_obj.search(search_domain)
        if not warehouses:
            log_info = _("No warehouse found.")
        elif len(warehouses) > 1:
            warehouses = False
            log_info = _("More than one warehouse with name {} found.").format(
                self.purchase_warehouse
            )
        return warehouses and warehouses[:1], log_info

    def _check_picking_type(self, warehouse):
        self.ensure_one()
        log_info = ""
        if self.purchase_picking_type_id:
            return self.purchase_picking_type_id, log_info
        picking_type_obj = self.env["stock.picking.type"]
        search_domain = [
            ("code", "=", "incoming"),
            ("warehouse_id", "=", warehouse.id),
        ]
        picking_types = picking_type_obj.search(search_domain)
        if not picking_types:
            log_info = _("No picking type found.")
        elif len(picking_types) > 1:
            picking_types = False
            log_info = _("More than one picking type with warehouse {} found.").format(
                warehouse
            )
        return picking_types and picking_types[:1], log_info

    def _create_purchase_order(self):
        purchase_order_obj = self.env["purchase.order"]
        values = self._purchase_order_values()
        purchase = purchase_order_obj.create(values)
        return purchase

    def _create_purchase_order_line(self, purchase_order):
        purchase_order.order_line = [
            (
                0,
                0,
                {
                    "product_id": self.purchase_product_id.id,
                    "product_qty": self.purchase_ordered_qty or self.purchase_qty_done,
                    "qty_received": self.purchase_qty_done,
                    "product_uom": self.purchase_product_id.uom_id.id,
                    "name": self.purchase_product_id.display_name,
                    "order_id": purchase_order,
                    "price_unit": self.purchase_price_unit,
                    "discount": self.purchase_discount,
                },
            )
        ]

    def _purchase_order_values(self):
        self.ensure_one()
        new_po = self.env["purchase.order"].new(
            {
                "partner_id": self.purchase_supplier_id.id,
                "picking_type_id": self.purchase_picking_type_id.id,
                "partner_ref": self.purchase_origin,
                "date_order": self.purchase_create_date,
            }
        )
        for partner_onchange_method in new_po._onchange_methods["partner_id"]:
            partner_onchange_method(new_po)
        for pick_type_onchange_method in new_po._onchange_methods["picking_type_id"]:
            pick_type_onchange_method(new_po)
        order_vals = new_po._convert_to_write(new_po._cache)
        return order_vals
