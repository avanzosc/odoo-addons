# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import check_number, convert2date


class SaleOrderImport(models.Model):
    _inherit = "sale.order.import"

    historical = fields.Boolean(
        copy=False,
        index=True,
    )

    @staticmethod
    def _get_column_value(row_values, column):
        value = row_values.get(column)
        if value not in (None, ""):
            return value
        normalized_column = "".join(str(column or "").strip().lower().split())
        for key, key_value in row_values.items():
            normalized_key = "".join(str(key or "").strip().lower().split())
            if normalized_key == normalized_column:
                return key_value
        return ""

    @staticmethod
    def _to_float(value):
        if value in (None, ""):
            return 0.0
        number = check_number(value)
        if number is False:
            return 0.0
        return float(number)

    @staticmethod
    def _to_bool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, int | float):
            return bool(value)
        text = str(value or "").strip().lower()
        return text in {"1", "true", "t", "yes", "y", "x"}

    def _get_line_fields_values(self, row_values):
        values = super()._get_line_fields_values(row_values)
        get_value = self._get_column_value

        def first_value(*columns):
            for column in columns:
                value = get_value(row_values, column)
                if value not in (None, ""):
                    return value
            return None

        def string_value(current, *columns):
            value = first_value(*columns)
            if value in (None, ""):
                return current or ""
            return str(value).strip()

        def float_value(current, *columns):
            value = first_value(*columns)
            if value in (None, ""):
                return current
            return self._to_float(value)

        def bool_value(current, *columns):
            value = first_value(*columns)
            if value in (None, ""):
                return current
            return self._to_bool(value)

        confirmation_date = first_value("Confirmation Date")
        date_order = first_value("Order Date", "FechaPedido")
        delivery_date = first_value("Expected Shipment Date", "FechaEntrega")
        quantity_ordered = first_value("QuantityOrdered", "Cantidad")
        item_price = first_value("Item Price", "PrecioUnitario")
        total_amount = first_value("Item Total", "TotalImportePedido")
        values.update(
            {
                "salesorder_external_id": string_value(
                    values.get("salesorder_external_id"),
                    "SalesOrder ID",
                    "Sales Order ID",
                ),
                "origin_import": string_value(values.get("origin_import"), "Origin"),
                "sales_team_import": string_value(
                    values.get("sales_team_import"),
                    "Equipo de ventas (team_id)",
                    "Equipo de ventas(team_id)",
                    "Sales Channel",
                ),
                "currency_code_import": string_value(
                    values.get("currency_code_import"), "Currency Code"
                ),
                "entity_discount_percent": float_value(
                    values.get("entity_discount_percent"), "Entity Discount Percent"
                ),
                "client_order_ref": string_value(
                    values.get("client_order_ref"),
                    "SalesOrder Number",
                    "NumeroPedidoCliente",
                ),
                "product_name": string_value(
                    values.get("product_name"), "Item Name", "NombreProducto"
                ),
                "product_code": string_value(
                    values.get("product_code"), "SKU", "CodigoProducto"
                ),
                "product_barcode": string_value(
                    values.get("product_barcode"), "EAN", "CodigoBarrasProducto"
                ),
                "customer_name": string_value(
                    values.get("customer_name"), "Customer Name", "NombreCliente"
                ),
                "customer_reference": string_value(
                    values.get("customer_reference"), "Customer ID", "ReferenciaCliente"
                ),
                "order_name": string_value(
                    values.get("order_name"),
                    "SalesOrder Number",
                    "NumeroPedidoCliente",
                ),
                "confirmation_date": (
                    convert2date(confirmation_date)
                    if confirmation_date
                    else values.get("confirmation_date")
                ),
                "date_order": (
                    convert2date(date_order) if date_order else values.get("date_order")
                ),
                "delivery_date": (
                    convert2date(delivery_date)
                    if delivery_date
                    else values.get("delivery_date")
                ),
                "discount": float_value(values.get("discount"), "Discount"),
                "product_uos_qty": float_value(
                    values.get("product_uos_qty"), "QuantityOrdered", "Cantidad"
                ),
                "quantity_invoiced": float_value(
                    values.get("quantity_invoiced"), "QuantityInvoiced"
                ),
                "quantity_packed": float_value(
                    values.get("quantity_packed"), "QuantityPacked"
                ),
                "product_uom_name": string_value(
                    values.get("product_uom_name"),
                    "Usage unit (UOM)",
                    "Usage Unit(UOM)",
                    "Usage unit",
                ),
                "usage_unit": string_value(
                    values.get("usage_unit"),
                    "Usage unit (UOM)",
                    "Usage Unit(UOM)",
                    "Usage unit",
                ),
                "warehouse_name_import": string_value(
                    values.get("warehouse_name_import"), "Warehouse Name"
                ),
                "line_type": string_value(
                    values.get("line_type"), "LineType", "Status"
                ),
                "salesman_name": string_value(
                    values.get("salesman_name"), "Sales Person"
                ),
                "invoiced": bool_value(values.get("invoiced"), "Invoiced"),
                "quantity": (
                    self._to_float(quantity_ordered)
                    if quantity_ordered not in (None, "")
                    else values.get("quantity")
                ),
                "price_unit": (
                    self._to_float(item_price)
                    if item_price not in (None, "")
                    else values.get("price_unit")
                ),
                "total_order_amount": (
                    self._to_float(total_amount)
                    if self.historical and total_amount not in (None, "")
                    else values.get("total_order_amount")
                ),
                "line_subtotal_amount": float_value(
                    values.get("line_subtotal_amount"), "SubTotal"
                ),
                "item_total_amount": float_value(
                    values.get("item_total_amount"),
                    "Item Total",
                    "TotalImportePedido",
                ),
                "line_total_amount": float_value(
                    values.get("line_total_amount"), "Line Total", "Total"
                ),
                "payment_terms_import": string_value(
                    values.get("payment_terms_import"), "Payment Terms"
                ),
                "payment_terms_label_import": string_value(
                    values.get("payment_terms_label_import"), "Payment Terms Label"
                ),
                "purchase_order_import": string_value(
                    values.get("purchase_order_import"), "PurchaseOrder"
                ),
                "exchange_rate_import": float_value(
                    values.get("exchange_rate_import"), "Exchange Rate"
                ),
                "is_inclusive_tax_import": bool_value(
                    values.get("is_inclusive_tax_import"), "Is Inclusive Tax"
                ),
            }
        )
        return values

    def button_open_import_line(self):
        self.ensure_one()
        action = super().button_open_import_line()
        base_domain = action.get("domain") or []
        action["domain"] = expression.AND(
            [base_domain, [("historical", "=", self.historical)]]
        )
        context = action.get("context") or {}
        if isinstance(context, str):
            context = safe_eval(context)
        context.update(
            {
                "search_default_historical_true": 1 if self.historical else 0,
                "search_default_historical_false": 0 if self.historical else 1,
            }
        )
        action["context"] = context
        return action

    def action_process(self):
        if self.filtered("historical"):
            raise UserError(_("Historical imports cannot be processed."))
        return super().action_process()
