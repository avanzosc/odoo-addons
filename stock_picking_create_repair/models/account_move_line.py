# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_repair = fields.Boolean(
        string="Is repair", related="sale_line_id.is_repair", store=True, copy=False
    )
    product_rma_ids = fields.Many2many(
        string="Repair orders products",
        comodel_name="product.rma",
        compute="_compute_product_rma_ids",
    )
    amount_products_rmas = fields.Monetary(
        string="Amount repair orders",
        currency_field="currency_id",
        compute="_compute_product_rma_ids",
    )

    def _compute_product_rma_ids(self):
        for line in self:
            if not line.sale_line_id or not line.is_repair:
                line.product_rma_ids = [(6, 0, [])]
                line.amount_products_rmas = 0
            else:
                products = []
                for repair in line.sale_line_id.repair_order_ids.filtered(
                    lambda x: x.state in ("done", "2binvoiced")
                    and x.invoice_id == line.move_id
                ):
                    for operation in repair.operations:
                        if repair.invoice_method != "none":
                            price_subtotal = operation.price_subtotal
                        else:
                            price_subtotal = 0
                        products = self._update_array_products(
                            products,
                            operation.product_id,
                            operation.product_uom,
                            operation.product_uom_qty,
                            price_subtotal,
                        )
                    for fee_line in repair.fees_lines:
                        if repair.invoice_method != "none":
                            price_subtotal = fee_line.price_subtotal
                        else:
                            price_subtotal = 0
                        products = self._update_array_products(
                            products,
                            fee_line.product_id,
                            fee_line.product_uom,
                            fee_line.product_uom_qty,
                            price_subtotal,
                        )
                    repair.invoice_id = line.move_id.id
                if not products:
                    line.product_rma_ids = [(6, 0, [])]
                    line.amount_products_rmas = 0
                else:
                    product_rma_ids = []
                    for product in products:
                        product_rma_ids.append(
                            (
                                0,
                                0,
                                {
                                    "sale_line_id": line.sale_line_id.id,
                                    "product_rma": product[0].name,
                                    "product_uom_id": product[1].get("uom").id,
                                    "quantity": product[1].get("qty"),
                                    "amount": product[1].get("subtotal"),
                                    "currency_id": line.currency_id.id,
                                },
                            )
                        )
                    line.product_rma_ids = product_rma_ids
                    line.amount_products_rmas = sum(
                        line.product_rma_ids.mapped("amount")
                    )

    def _update_array_products(self, array, product, uom, qty, subtotal):
        found = False
        for element in array:
            if element[0] == product:
                if subtotal != 0:
                    found = True
                    new_qty = element[1].get("qty") + qty
                    new_subtotal = element[1].get("subtotal") + subtotal
                    element[1]["qty"] = new_qty
                    element[1]["subtotal"] = new_subtotal
                else:
                    element_subtotal = element[1].get("subtotal")
                    if element_subtotal == 0:
                        found = True
                        new_qty = element[1].get("qty") + qty
                        element[1]["qty"] = new_qty
        if not found:
            array.append((product, {"uom": uom, "qty": qty, "subtotal": subtotal}))
        return array

    @api.model_create_multi
    def create(self, vals_list):
        result = super().create(vals_list)
        for line in result:
            vals = {}
            if line.sale_line_ids and len(line.sale_line_ids) == 1:
                sale_line = line.sale_line_ids[0]
                if sale_line.is_repair and sale_line.product_to_repair_id:
                    vals = {
                        "product_id": sale_line.product_to_repair_id.id,
                        "name": sale_line.product_to_repair_id.name,
                    }
                    repair_vals = {"invoice_id": line.move_id.id}
                    repairs = sale_line.repair_order_ids.filtered(
                        lambda x: not x.invoice_id and x.state == "done"
                    )
                    if repairs:
                        repairs.write(repair_vals)
                    repairs = sale_line.repair_order_ids.filtered(
                        lambda x: not x.invoice_id and x.state == "2binvoiced"
                    )
                    if repairs:
                        repair_vals["state"] = "done"
                        repair_vals["invoiced"] = True
                        repairs.write(repair_vals)
            if vals:
                line.write(vals)
        return result
