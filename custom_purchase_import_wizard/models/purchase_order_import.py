# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import pytz
import xlrd

from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import convert2str


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

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            purchase_supplier_code = row_values.get("CodigoProveedor", "")
            purchase_supplier_name = row_values.get("NombreProveedor", "")
            purchase_date_planned = row_values.get("Fecha", "")
            timezone = pytz.timezone(self._context.get("tz") or "UTC")
            purchase_date_planned = xlrd.xldate.xldate_as_datetime(
                purchase_date_planned, 0
            )
            purchase_date_planned = timezone.localize(purchase_date_planned).astimezone(
                pytz.UTC
            )
            purchase_date_planned = purchase_date_planned.replace(tzinfo=None)
            purchase_origin = row_values.get("Entrada", "")
            purchase_product_code = row_values.get("CodigoProducto", "")
            purchase_product_name = row_values.get("NombreProducto", "")
            purchase_ordered_qty = row_values.get("KgProveedor", "")
            purchase_qty_done = row_values.get("KgNeto", "")
            purchase_license_plate = row_values.get("Matricula", "")
            purchase_warehouse = row_values.get("CodigoAlmacen", "")
            purchase_shipping_method = row_values.get("MetodoEnvio", "")
            log_info = ""
            if not purchase_warehouse:
                return {}
            values.update(
                {
                    "purchase_supplier_code": convert2str(purchase_supplier_code),
                    "purchase_supplier_name": purchase_supplier_name.title(),
                    "purchase_date_planned": purchase_date_planned,
                    "purchase_origin": convert2str(purchase_origin),
                    "purchase_product_code": convert2str(purchase_product_code),
                    "purchase_product_name": convert2str(purchase_product_name),
                    "purchase_ordered_qty": purchase_ordered_qty,
                    "purchase_qty_done": purchase_qty_done,
                    "purchase_license_plate": convert2str(purchase_license_plate),
                    "purchase_warehouse": convert2str(purchase_warehouse),
                    "purchase_shipping_method": convert2str(purchase_shipping_method),
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
        states={"done": [("readonly", True)]},
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
    purchase_date_planned = fields.Datetime(
        string="Date",
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
    purchase_ordered_qty = fields.Char(
        string="Ordered Qty",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_qty_done = fields.Char(
        string="Qty Done",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_license_plate = fields.Char(
        string="License Plate",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_warehouse = fields.Char(
        string="Warehouse",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_shipping_method = fields.Char(
        string="Shipping Method",
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
    purchase_requisition_id = fields.Many2one(
        string="Purchase Requisition",
        comodel_name="purchase.requisition",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_requisition_line_id = fields.Many2one(
        string="Purchase Requisition Line",
        comodel_name="purchase.requisition.line",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    purchase_product_cost = fields.Float(
        string="Product Cost",
        states={"done": [("readonly", True)]},
        copy=False,
        digits="Standard Cost Decimal Precision",
    )
    purchase_product_shipping_cost = fields.Float(
        string="Shipping Cost",
        states={"done": [("readonly", True)]},
        copy=False,
        digits="Standard Cost Decimal Precision",
    )
    purchase_shipping_method_id = fields.Many2one(
        string="Shipping Method",
        comodel_name="delivery.carrier",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    @api.onchange("purchase_requisition_id")
    def onchange_purchase_requisition_id(self):
        self.purchase_requisition_line_id = False
        if self.purchase_requisition_id and self.purchase_product_id:
            line = self.purchase_requisition_id.line_ids.filtered(
                lambda c: c.product_id == self.purchase_product_id
            )
            if line and len(line) == 1:
                self.purchase_requisition_line_id = line.id

    @api.onchange("purchase_requisition_line_id")
    def onchange_purchase_requisition_line_id(self):
        self.purchase_product_cost = 0
        self.purchase_product_shipping_cost = 0
        if self.purchase_requisition_line_id:
            self.purchase_product_cost = self.purchase_requisition_line_id.price_unit
            self.purchase_product_shipping_cost = (
                self.purchase_requisition_line_id.shipping_cost
            )
            self.purchase_requisition_id = (
                self.purchase_requisition_line_id.requisition_id.id
            )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda ln: ln.state != "done"):
            log_info = ""
            origin = (
                picking_type
            ) = product = supplier = warehouse = shipping_method = False
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
                if (line.purchase_requisition_id) and not (
                    line.purchase_requisition_line_id
                ):
                    line.onchange_purchase_requisition_id()
                    if not line.purchase_requisition_line_id:
                        log_info += _(
                            "Error: The contract has no line " + "with that product"
                        )
                if line.purchase_shipping_method:
                    (
                        shipping_method,
                        log_info_shipping_method,
                    ) = line._check_shipping_method()
                    if log_info_shipping_method:
                        log_info += log_info_shipping_method
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
                    "purchase_shipping_method_id": (
                        shipping_method and shipping_method.id
                    ),
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
        origins = []
        for line in self.filtered(lambda ln: ln.state not in ("error", "done")):
            if line.action == "create":
                if not line.purchase_origin:
                    log_info = ""
                    purchase = line._create_purchase_order()
                    line._create_purchase_order_line(purchase_order=purchase)
                if line.purchase_origin and line.purchase_origin not in origins:
                    if self.filtered(
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
                    purchase.date_planned = line.purchase_date_planned
                    purchase.button_confirm()
                    pickings = self.env["stock.picking"].search(
                        [("purchase_id", "=", purchase.id)]
                    )
                    pickings.write(
                        {
                            "shipping_cost": line.purchase_product_shipping_cost,
                            "custom_date_done": line.purchase_date_planned,
                            "origin": line.purchase_origin,
                            "license_plate": line.purchase_license_plate,
                        }
                    )
                    pickings.button_force_done_detailed_operations()
                    pickings.button_validate()
                    for orderlines in purchase.order_line:
                        move = pickings.move_ids_without_package.filtered(
                            lambda c: c.purchase_line_id == orderlines
                        )
                        move.write(
                            {
                                "standard_price": orderlines.price_unit,
                                "amount": (orderlines.price_unit * move.quantity_done),
                            }
                        )
                        ml = move.move_line_ids
                        ml.write(
                            {
                                "qty_done": move.purchase_line_id.qty_done,
                                "standard_price": orderlines.price_unit,
                                "amount": (move.purchase_line_id.qty_done)
                                * (orderlines.price_unit),
                            }
                        )
            else:
                continue
            state = "error" if log_info else "done"
            line.write(
                {"purchase_order_id": purchase.id, "log_info": log_info, "state": state}
            )
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "purchase_order_id": purchase.id,
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
        if self.purchase_supplier_id:
            return self.purchase_supplier_id, log_info
        supplier_obj = self.env["res.partner"]
        if self.purchase_supplier_code:
            search_domain = [("ref", "=", self.purchase_supplier_code)]
        else:
            search_domain = [("name", "=", self.purchase_supplier_name)]
        suppliers = supplier_obj.search(search_domain)
        if not suppliers:
            suppliers = False
            log_info = _("Error: No supplier found.")
        elif len(suppliers) > 1:
            suppliers = False
            log_info = _("Error: More than one supplier found.")
        return suppliers and suppliers[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.purchase_product_id:
            return self.purchase_product_id, log_info
        product_obj = self.env["product.product"]
        if self.purchase_product_code:
            search_domain = [("default_code", "=", self.purchase_product_code)]
        else:
            search_domain = [("name", "=", self.purchase_product_name)]
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
            products = False
            log_info = _(
                "Error: More than one product with the same name or " + "code found."
            ).format(self.purchase_product_name, self.purchase_product_code)
        return products and products[:1], log_info

    def _check_warehouse(self):
        self.ensure_one()
        log_info = ""
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

    def _check_shipping_method(self):
        self.ensure_one()
        log_info = ""
        if self.purchase_shipping_method_id:
            return self.purchase_shipping_method_id, log_info
        shipping_method_obj = self.env["delivery.carrier"]
        search_domain = [("name", "=", self.purchase_shipping_method)]
        shipping_methods = shipping_method_obj.search(search_domain)
        if not shipping_methods:
            shipping_methods = False
            log_info = _("Error: No shipping method found.")
        elif len(shipping_methods) > 1:
            shipping_methods = False
            log_info = _("Error: More than one shipping method found.")
        return shipping_methods and shipping_methods[:1], log_info

    def _create_purchase_order(self):
        purchase_order_obj = self.env["purchase.order"]
        values = self._purchase_order_values()
        if self.purchase_requisition_id:
            values.update({"requisition_id": self.purchase_requisition_id.id})
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
                        "qty_done": self.purchase_qty_done,
                        "product_uom": self.purchase_product_id.uom_id.id,
                        "name": self.purchase_product_id.display_name,
                        "order_id": purchase_order,
                        "price_unit": self.purchase_product_cost,
                    },
                )
            ]

    def _purchase_order_values(self):
        return {
            "partner_id": self.purchase_supplier_id.id,
            "picking_type_id": self.purchase_picking_type_id.id,
            "partner_ref": self.purchase_origin,
            "date_planned": self.purchase_date_planned,
            "shipping_cost": self.purchase_product_shipping_cost,
            "shipping_method_id": self.purchase_shipping_method_id.id,
        }
