# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import unicodedata
from datetime import datetime

import pytz
import xlrd

from odoo import _, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import (convert2date,
                                                               convert2str)


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
        comodel_name="res.company",
        string="Company",
        index=True,
    )
    warehouse_id = fields.Many2one(string="Warehouse", comodel_name="stock.warehouse")

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            purchase_supplier_code = row_values.get("CodigoProveedor", "")
            purchase_supplier_name = row_values.get("NombreProveedor", "")
            purchase_create_date = row_values.get("FechaCreada", "")
            purchase_date_confirm = row_values.get("FechaConfirmada", "")
            purchase_origin = row_values.get("Entrada", "")
            purchase_product_code = row_values.get("CodigoProducto", "")
            purchase_product_name = row_values.get("NombreProducto", "")
            purchase_ordered_qty = row_values.get("CantidadPedida", "")
            purchase_qty_done = row_values.get("CantidadRecibida", "")
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
                        purchase_create_date
                    ) if purchase_create_date else False,
                    "purchase_date_confirm": convert2date(
                        purchase_date_confirm
                    ) if purchase_date_confirm else False,
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
        string="Action",
        selection=[
            ("create", "Create"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    purchase_order_id = fields.Many2one(
        string="Purchase Order", comodel_name="purchase.order"
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
        string="Origin",
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

    def action_validate(self):
        line_values = super().action_validate()
        for line in self.filtered(lambda ln: ln.state != "done"):
            log_info = ""
            origin = picking_type = product = supplier = warehouse = False
            if line.purchase_origin:
                origin, log_info = line._check_origin()
                if log_info:
                    update_values = {
                        "purchase_origin": origin,
                        "log_info": log_info,
                        "state": "error",
                        "action": "nothing",
                    }
            if not log_info:
                supplier, log_info_supplier = line._check_supplier()
                if log_info_supplier:
                    log_info += log_info_supplier
                product, log_info_product = line._check_product()
                if log_info_product:
                    log_info += log_info_product
                warehouse, log_info_warehouse = line._check_warehouse()
                if log_info_warehouse:
                    log_info += log_info_warehouse
                if not log_info_warehouse and warehouse:
                    picking_type, log_info_picking_type = line._check_picking_type(
                        warehouse=warehouse
                    )
                    if log_info_picking_type:
                        log_info += log_info_picking_type
                state = "error" if log_info else "pass"
                action = "nothing"
                if state != "error":
                    action = "create"
                update_values = {
                    "purchase_origin": origin,
                    "purchase_supplier_id": supplier and supplier.id,
                    "purchase_product_id": product and product.id,
                    "purchase_warehouse_id": warehouse and warehouse.id,
                    "purchase_picking_type_id": (picking_type and picking_type.id),
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
        line_values = super().action_process()
        origins = []
        for line in self.filtered(lambda ln: ln.state not in ("error", "done")):
            purchase = False
            if line.action == "create":
                if not line.purchase_origin:
                    log_info = ""
                    purchase = line._create_purchase_order()
                    line._create_purchase_order_line(purchase_order=purchase)
                if line.purchase_origin and line.purchase_origin not in origins:
                    if line.import_id.import_line_ids.filtered(
                        lambda ln: ln.purchase_origin == line.purchase_origin
                        and ln.state == "error"
                    ):
                        log_info = _(
                            "Error: There is another line with the same"
                            + " origin document with some errors."
                        )
                    else:
                        origin, log_info = line._check_origin()
                        if not log_info:
                            origins.append(origin)
                            purchase = line._create_purchase_order()
                            same_origin = self.filtered(
                                lambda ln: ln.purchase_origin == line.purchase_origin
                            )
                            for record in same_origin:
                                record._create_purchase_order_line(
                                    purchase_order=purchase
                                )
                if purchase:
                    purchase.button_confirm()
                    purchase.date_approve = line.purchase_date_confirm.date()
            else:
                continue
            state = "error" if log_info else "done"
            line.write(
                {"purchase_order_id": purchase.id if purchase else False, "log_info": log_info, "state": state}
            )
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "purchase_order_id": purchase.id if purchase else False,
                        "log_info": log_info,
                        "state": state,
                    },
                )
            )
        return line_values

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
        search_domain = []
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
        search_domain = []
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
            search_domain = [("name", "=ilike", name)]
        elif self.purchase_product_code and self.purchase_product_name:
            search_domain = [
                "|",
                ("name", "=ilike", name),
                ("default_code", "=", self.purchase_product_code),
            ]
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
            if self.purchase_product_code and self.purchase_product_name:
                search_domain = [
                    ("name", "=ilike", name),
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
            warehouses = False
            log_info = _("Error: No warehouse found.")
        elif len(warehouses) > 1:
            warehouses = False
            log_info = _("Error: More than one warehouse with name {} found.").format(
                self.purchase_warehouse
            )
        return warehouses and warehouses[:1], log_info

    def _check_picking_type(self, warehouse=False):
        self.ensure_one()
        log_info = ""
        if self.purchase_picking_type_id:
            return self.purchase_picking_type_id, log_info
        picking_type_obj = self.env["stock.picking.type"]
        search_domain = [("code", "=", "incoming")]
        if warehouse:
            search_domain = expression.AND(
                [[("warehouse_id", "=", warehouse.id)], search_domain]
            )
        picking_types = picking_type_obj.search(search_domain)
        if not picking_types:
            picking_types = False
            log_info = _("Error: No picking type found.")
        elif len(picking_types) > 1:
            picking_types = False
            log_info = _(
                "Error: More than one picking type with warehouse {} found."
            ).format(warehouse)
        return picking_types and picking_types[:1], log_info

    def _create_purchase_order(self):
        purchase_order_obj = self.env["purchase.order"]
        values = self._purchase_order_values()
        purchase = purchase_order_obj.create(values)
        return purchase

    def _create_purchase_order_line(self, purchase_order=False):
        if purchase_order:
            if not self.purchase_ordered_qty and self.purchase_qty_done:
                self.purchase_ordered_qty = self.purchase_qty_done
            purchase_order.order_line = [
                (
                    0,
                    0,
                    {
                        "product_id": self.purchase_product_id.id,
                        "product_qty": self.purchase_ordered_qty,
                        "qty_received": self.purchase_qty_done,
                        "product_uom": self.purchase_product_id.uom_id.id,
                        "name": self.purchase_product_id.display_name,
                        "order_id": purchase_order,
                        "price_unit": self.purchase_price_unit,
                        "discount": self.purchase_discount,
                        "date_planned": self.purchase_create_date,
                    },
                )
            ]

    def _purchase_order_values(self):
        return {
            "partner_id": self.purchase_supplier_id.id,
            "picking_type_id": self.purchase_picking_type_id.id,
            "partner_ref": self.purchase_origin,
            "date_order": self.purchase_create_date,
        }
