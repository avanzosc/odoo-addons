# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp
from odoo.addons.base_import_wizard.models.base_import import (
    check_number,
    convert2str,
    convert2date,
)


class StockWarehouseOrderpointImport(models.Model):
    _name = "stock.warehouse.orderpoint.import"
    _inherit = "base.import"
    _description = "Minimum Inventory Rule Import Wizard"

    import_line_ids = fields.One2many(
        comodel_name="stock.warehouse.orderpoint.import.line",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Warehouse',
        states={"done": [("readonly", True)]},
        copy=False,
    )
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',
        states={"done": [("readonly", True)]},
        copy=False,
    )
    orderpoint_count = fields.Integer(
        compute="_compute_orderpoint_count",
    )

    def _compute_orderpoint_count(self):
        for record in self:
            record.orderpoint_count = len(
                record.mapped("import_line_ids.orderpoint_id")
            )


    def _get_line_values(self, row_values=False, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values, datemode=datemode)
        if row_values:
            log_infos = []
            product_name = row_values.get("Producto", "")
            product_code = row_values.get("Referencia interna", "")
            if not product_name and not product_code:
                return {}
            orderpoint_name = row_values.get("Nombre", "")
            warehouse_name = row_values.get("Almacén", "")
            location_name = row_values.get("Ubicación", "")
            min_qty = row_values.get("Min", 0.0)
            max_qty = row_values.get("Max", 0.0)
            # qty_multiple = row_values.get("", 1.0)
            values.update(
                {
                    "product_code": convert2str(product_code),
                    "product_name": convert2str(product_name),
                    "orderpoint_name": convert2str(orderpoint_name),
                    "warehouse_name": convert2str(warehouse_name) or self.warehouse_id.name,
                    "warehouse_id": self.warehouse_id.id if not warehouse_name else False,
                    "location_name": convert2str(location_name) or self.location_id.display_name,
                    "location_id": self.location_id.id if not warehouse_name else False,
                    "product_min_qty": check_number(min_qty),
                    "product_max_qty": check_number(max_qty),
                    # "qty_multiple": check_number(qty_multiple),
                }
            )
            values.update(
                {
                    "log_info": "\n".join(log_infos),
                    "state": "error" if log_infos else "2validate",
                }
            )
        return values

    def button_open_import_line(self):
        action = super().button_open_import_line()
        action['context'].update({'import_hide': False})
        return action

    def button_open_orderpoint(self):
        self.ensure_one()
        orderpoints = self.mapped("import_line_ids.orderpoint_id")
        action = self.env["ir.actions.act_window"].for_xml_id(
            "stock", "action_orderpoint_form")
        action["domain"] = expression.AND(
            [[("id", "in", orderpoints.ids)], safe_eval(action.get("domain") or "[]")]
        )
        return action

class StockWarehouseOrderpointImportLine(models.Model):
    _name = "stock.warehouse.orderpoint.import.line"
    _inherit = "base.import.line"
    _description = "Minimum Inventory Rule Import Wizard Line"

    import_id = fields.Many2one(
        comodel_name="stock.warehouse.orderpoint.import",
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        states={"done": [("readonly", True)]},
        copy=False,
    )
    orderpoint_name = fields.Char(
        string='Minimum Inventory Rule Name',
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
    warehouse_name = fields.Char(
        string="Warehouse Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    location_name = fields.Char(
        string="Location Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Warehouse',
    )
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string='Product',
        domain=[('type', '=', 'product')],
    )
    product_min_qty = fields.Float(
        string="Minimum Quantity",
        digits=dp.get_precision('Product Unit of Measure'),
    )
    product_max_qty = fields.Float(
        string='Maximum Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    qty_multiple = fields.Float(
        string='Qty Multiple',
        digits=dp.get_precision('Product Unit of Measure'),
        default=1,
    )
    orderpoint_id = fields.Many2one(
        comodel_name="stock.warehouse.orderpoint",
        readonly=True,
        copy=False,
    )

    @api.multi
    def write(self, values):
        if not values.get("state", False):
            values.update({
                "state": "2validate",
            })
        return super(StockWarehouseOrderpointImportLine, self).write(values)

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        product_obj = self.env["product.product"].with_context(
            force_company_id=self.import_id.company_id.id)
        if self.product_id:
            return self.product_id, log_info
        else:
            search_domain = [
                ("default_code", "=", self.product_code),
            ]
        products = product_obj.search(search_domain)
        name_domain = [
            ("name", "=", self.product_name),
        ]
        if not products:
            search_domain = expression.OR(
                [
                    search_domain,
                    name_domain
                ]
            )
        elif len(products) > 1:
            search_domain = expression.AND(
                [
                    search_domain,
                    name_domain,
                ]
            )
        products = product_obj.search(search_domain)
        if not products:
            log_info = _("No product found.")
        elif len(products) > 1:
            products = False
            log_info = _("More than one product already exist.")
        return products and products[:1], log_info

    def _check_warehouse(self):
        self.ensure_one()
        log_info = ""
        if self.warehouse_id:
            return self.warehouse_id, log_info
        if not self.warehouse_name:
            log_info = (
                _("No warehouse found.") if not self.import_id.warehouse_id else
                log_info
            )
            return self.import_id.warehouse_id, log_info
        warehouse_obj = self.env["stock.warehouse"].with_context(
            force_company_id=self.import_id.company_id.id)
        search_domain = [
            ("name", "=", self.warehouse_name),
        ]
        warehouses = warehouse_obj.search(search_domain)
        if not warehouses:
            log_info = _("No warehouse found with name '{}' found.").format(
                self.warehouse_name
            )
        elif len(warehouses) > 1:
            warehouses = False
            log_info = _("More than one warehouse with name '{}' found.").format(
                self.warehouse_name
            )
        return warehouses and warehouses[:1], log_info

    def _check_location(self):
        self.ensure_one()
        log_info = ""
        if self.location_id:
            return self.location_id, log_info
        if not self.location_name:
            log_info = (
                _("No location found.") if not self.import_id.location_id else log_info
            )
            return self.import_id.location_id, log_info
        location_obj = self.env["stock.location"].with_context(
            force_company_id=self.import_id.company_id.id)
        search_domain = [
            ("complete_name", "ilike", self.location_name),
        ]
        locations = location_obj.search(search_domain)
        if not locations:
            log_info = _("No location with name '{}' found.").format(
                self.location_name
            )
        elif len(locations) > 1:
            locations = False
            log_info = _("More than one location with name '{}' found.").format(
                self.location_name
            )
        return locations and locations[:1], log_info

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        warehouse, log_info_warehouse = self._check_warehouse()
        if log_info_warehouse:
            log_infos.append(log_info_warehouse)
        location, log_info_location = self._check_location()
        if log_info_location:
            log_infos.append(log_info_location)
        state = "error" if log_infos else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "product_id": product and product.id,
                "warehouse_id": warehouse and warehouse.id,
                "location_id": location and location.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        log_infos = []
        if not self.product_id:
            log_infos.append(_("Product not selected."))
        if not self.warehouse_id:
            log_infos.append(_("Warehouse not selected."))
        if not self.location_id:
            log_infos.append(_("Location not selected."))
        if log_infos:
            update_values.update({
                "log_info": "\n".join(log_infos),
                "state": "error",
            })
            return update_values
        orderpoint = self.env["stock.warehouse.orderpoint"].create(
            self._product_orderpoint_values())
        update_values.update(
            {
                "orderpoint_id": orderpoint and orderpoint.id,
                "log_info": "",
                "state": "done",
            }
        )
        return update_values

    def _product_orderpoint_values(self):
        self.ensure_one()
        orderpoint_values =  {
            "product_id": self.product_id.id,
            "warehouse_id": self.warehouse_id.id,
            "location_id": self.location_id.id,
            "product_min_qty": self.product_min_qty,
            "product_max_qty": self.product_max_qty,
            "company_id": self.import_id.company_id.id,
        }
        if self.orderpoint_name:
            orderpoint_values.update({
                "name": self.orderpoint_name,
            })
        return orderpoint_values

    def action_open_form(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"].for_xml_id(
            "stock_orderpoint_import_wizard",
            "stock_warehouse_orderpoint_import_line_action"
        )
        action['views'] = [(
            self.env.ref("stock_orderpoint_import_wizard."
                         "stock_warehouse_orderpoint_import_line_view_form").id,
            "form")]
        action["res_id"] = self.id
        return action
